// CSV file path
const CSV_FILE = 'sola-luna-festival-timetable-complete.csv';

// Parse CSV data
function parseCSV(csv) {
    const lines = csv.trim().split('\n');
    const headers = lines[0].split(',');
    const data = [];

    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        if (values.length === headers.length) {
            const entry = {};
            headers.forEach((header, index) => {
                entry[header.trim()] = values[index].trim();
            });
            data.push(entry);
        }
    }

    return data;
}

// State
let timetableData = [];
let favorites = new Set();
let currentPage = 'artists';
let selectedDay = 'all'; // 'all' shows all days

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    loadFavorites();
    await loadTimetable();
    setupNavigation();
    setupSearch();
    renderArtists();
    updateFollowingCount();
});

// Load timetable from CSV file
async function loadTimetable() {
    try {
        // Add cache-busting parameter
        const response = await fetch(`${CSV_FILE}?v=${Date.now()}`);
        const csvText = await response.text();
        timetableData = parseCSV(csvText);
    } catch (error) {
        console.error('Failed to load timetable:', error);
        timetableData = [];
    }
}

// Local storage
function loadFavorites() {
    const stored = localStorage.getItem('sola-luna-favorites');
    if (stored) {
        favorites = new Set(JSON.parse(stored));
    }
}

function saveFavorites() {
    localStorage.setItem('sola-luna-favorites', JSON.stringify([...favorites]));
}

// Navigation
function setupNavigation() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const page = btn.dataset.page;
            showPage(page);
        });
    });
}

function showPage(page) {
    currentPage = page;

    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.page === page);
    });

    // Update pages
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    document.getElementById(`${page}-page`).classList.add('active');

    // Render schedule if needed
    if (page === 'schedule') {
        renderSchedule();
    }
}

// Make showPage globally available
window.showPage = showPage;

// Search
function setupSearch() {
    const searchInput = document.getElementById('artist-search');
    searchInput.addEventListener('input', (e) => {
        renderArtists(e.target.value.toLowerCase());
    });
}

// Get unique artists sorted alphabetically
function getUniqueArtists() {
    const artistMap = new Map();

    timetableData.forEach(entry => {
        const name = entry.Artist;
        // Skip break entries
        if (name.toLowerCase().startsWith('break') || name.toLowerCase() === 'opening ceremony' || name.toLowerCase() === 'end') {
            return;
        }

        if (!artistMap.has(name)) {
            artistMap.set(name, {
                performances: [],
                soundcloud: entry['SoundCloud Link'] || '',
                beatport: entry['Beatport Link'] || ''
            });
        }
        artistMap.get(name).performances.push(entry);
    });

    return Array.from(artistMap.entries())
        .sort((a, b) => a[0].localeCompare(b[0]))
        .map(([name, data]) => ({
            name,
            performances: data.performances,
            soundcloud: data.soundcloud,
            beatport: data.beatport
        }));
}

// Render artists
function renderArtists(searchQuery = '') {
    const container = document.getElementById('artists-list');
    const artists = getUniqueArtists();

    const filtered = searchQuery
        ? artists.filter(a => a.name.toLowerCase().includes(searchQuery))
        : artists;

    container.innerHTML = filtered.map(artist => {
        const isFollowing = favorites.has(artist.name);
        const performanceInfo = artist.performances
            .map(p => `${formatDate(p.Date)} ${p.Time}`)
            .join(' | ');
        const stages = [...new Set(artist.performances.map(p => p.Stage))].join(', ');

        // Build social links
        let socialLinks = '';
        if (artist.soundcloud) {
            socialLinks += `<a href="${artist.soundcloud}" target="_blank" class="social-link soundcloud" title="SoundCloud">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M11.56 8.87V17h8.76c1.85 0 3.35-1.57 3.35-3.5 0-1.93-1.5-3.5-3.35-3.5-.35 0-.68.05-1 .14C18.89 7.3 16.64 5 13.9 5c-.84 0-1.63.21-2.34.58v3.29zm-1.39-.33a5.87 5.87 0 0 0-.79-.09c-2.97 0-5.38 2.52-5.38 5.63 0 1.71.74 3.25 1.9 4.29V8.54zm-2.3.33v8.47c.43.14.89.22 1.36.22.28 0 .55-.03.82-.08V8.73a4.47 4.47 0 0 0-2.18.14zM5.44 9.57v7.87c.35.15.72.26 1.1.33V9.29c-.4.07-.77.16-1.1.28zm-2.19.63v6.77c.35.22.72.4 1.1.54V9.67c-.39.14-.76.32-1.1.53zm-2.16 1.45v4.2c.42.42.9.77 1.43 1.03v-5.87a4.54 4.54 0 0 0-1.43.64z"/></svg>
            </a>`;
        }
        if (artist.beatport) {
            socialLinks += `<a href="${artist.beatport}" target="_blank" class="social-link beatport" title="Beatport">
                <svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.429 13.295c-.347-.26-.807-.317-1.197-.2l-2.755.78a3.79 3.79 0 0 0-.793-1.127c.26-.39.52-.78.78-1.17.26-.347.217-.823-.087-1.127a.852.852 0 0 0-1.17-.087l-1.69 1.257a3.84 3.84 0 0 0-1.56-.65V8.303c0-.433-.347-.78-.78-.78s-.78.347-.78.78v2.668a3.827 3.827 0 0 0-1.56.65L8.147 10.364a.85.85 0 0 0-1.17.087c-.304.304-.347.78-.087 1.127.26.39.52.78.78 1.17a3.79 3.79 0 0 0-.793 1.127l-2.756-.78c-.39-.117-.85-.06-1.197.2-.347.26-.52.693-.433 1.083l.693 3.016c.087.39.39.693.78.78.087.017.173.03.26.03.303 0 .607-.13.823-.347l1.82-1.82c.173.173.347.347.563.477l-.91 2.798c-.13.39-.017.823.26 1.083.26.26.693.39 1.083.26l2.798-.91c.173.217.347.39.563.563l-1.82 1.82a.877.877 0 0 0-.087 1.127c.217.303.563.477.91.477.087 0 .173-.017.26-.03l3.016-.693c.39-.087.693-.39.78-.78l.78-2.755c.347.087.693.13 1.04.13.346 0 .693-.043 1.04-.13l.78 2.756c.086.39.39.693.78.78l3.016.693c.087.013.173.03.26.03.347 0 .693-.173.91-.477a.877.877 0 0 0-.087-1.127l-1.82-1.82c.217-.173.39-.347.563-.563l2.798.91c.39.13.823.017 1.083-.26.26-.26.39-.693.26-1.083l-.91-2.798c.217-.13.39-.304.563-.477l1.82 1.82c.217.217.52.347.823.347.087 0 .173-.013.26-.03.39-.087.693-.39.78-.78l.693-3.016c.087-.39-.086-.823-.433-1.083zm-9.252 5.33c-1.3 0-2.362-1.04-2.362-2.362s1.04-2.363 2.362-2.363 2.363 1.04 2.363 2.363-1.04 2.362-2.363 2.362z"/></svg>
            </a>`;
        }

        return `
            <div class="artist-card">
                <div class="artist-info">
                    <div class="artist-name-row">
                        <span class="artist-name">${artist.name}</span>
                        ${socialLinks ? `<div class="social-links">${socialLinks}</div>` : ''}
                    </div>
                    <div class="artist-details">
                        <span class="artist-stage">${stages}</span> - ${performanceInfo}
                    </div>
                </div>
                <button class="follow-btn ${isFollowing ? 'following' : ''}"
                        onclick="toggleFollow('${escapeHtml(artist.name)}')">
                    ${isFollowing ? 'Following' : 'Follow'}
                </button>
            </div>
        `;
    }).join('');

    if (filtered.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No artists found</p></div>';
    }
}

// Toggle follow
function toggleFollow(artistName) {
    if (favorites.has(artistName)) {
        favorites.delete(artistName);
    } else {
        favorites.add(artistName);
    }
    saveFavorites();
    renderArtists(document.getElementById('artist-search').value.toLowerCase());
    updateFollowingCount();
}

window.toggleFollow = toggleFollow;

// Update following count
function updateFollowingCount() {
    document.getElementById('following-count').textContent = favorites.size;
}

// Format date
function formatDate(dateStr) {
    const [day, month] = dateStr.split('/');
    const months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${parseInt(day)} ${months[parseInt(month)]}`;
}

function formatDateFull(dateStr) {
    const [day, month] = dateStr.split('/');
    const months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const dayInt = parseInt(day);
    const monthInt = parseInt(month);
    const year = monthInt === 12 ? 2025 : 2026;
    return `${months[monthInt]} ${dayInt}, ${year}`;
}

// Get favorite performances sorted by time
function getFavoritePerformances() {
    return timetableData
        .filter(entry => favorites.has(entry.Artist))
        .map(entry => {
            const [day, month] = entry.Date.split('/');
            const [hours, minutes] = entry.Time.split(':');
            const year = parseInt(month) === 12 ? 2025 : 2026;
            const timestamp = new Date(year, parseInt(month) - 1, parseInt(day), parseInt(hours), parseInt(minutes)).getTime();
            return { ...entry, timestamp };
        })
        .sort((a, b) => a.timestamp - b.timestamp);
}

// Get unique days from favorites
function getUniqueDays(performances) {
    const days = [...new Set(performances.map(p => p.Date))];
    return days.sort((a, b) => {
        const [dayA, monthA] = a.split('/');
        const [dayB, monthB] = b.split('/');
        const yearA = parseInt(monthA) === 12 ? 2025 : 2026;
        const yearB = parseInt(monthB) === 12 ? 2025 : 2026;
        const dateA = new Date(yearA, parseInt(monthA) - 1, parseInt(dayA));
        const dateB = new Date(yearB, parseInt(monthB) - 1, parseInt(dayB));
        return dateA - dateB;
    });
}

// Render schedule
function renderSchedule() {
    const performances = getFavoritePerformances();
    const emptyState = document.getElementById('empty-schedule');
    const scheduleContent = document.getElementById('schedule-content');

    if (performances.length === 0) {
        emptyState.style.display = 'block';
        scheduleContent.style.display = 'none';
        return;
    }

    emptyState.style.display = 'none';
    scheduleContent.style.display = 'block';

    const days = getUniqueDays(performances);

    // Validate selectedDay - reset to 'all' if invalid
    if (selectedDay !== 'all' && !days.includes(selectedDay)) {
        selectedDay = 'all';
    }

    renderDayTabs(days);

    // Filter performances based on selected day
    const filteredPerformances = selectedDay === 'all'
        ? performances
        : performances.filter(p => p.Date === selectedDay);

    renderTimeline(filteredPerformances);
}

// Render day tabs
function renderDayTabs(days) {
    const container = document.getElementById('day-tabs');

    // Add "All Days" tab first
    let html = `
        <button class="day-tab ${selectedDay === 'all' ? 'active' : ''}"
                onclick="selectDay('all')">
            All Days
        </button>
    `;

    // Add individual day tabs
    html += days.map(day => `
        <button class="day-tab ${day === selectedDay ? 'active' : ''}"
                onclick="selectDay('${day}')">
            ${formatDate(day)}
        </button>
    `).join('');

    container.innerHTML = html;
}

function selectDay(day) {
    selectedDay = day;
    renderSchedule();
}

window.selectDay = selectDay;

// Render timeline
function renderTimeline(performances) {
    const container = document.getElementById('timeline');

    if (performances.length === 0) {
        container.innerHTML = '<div class="empty-state"><p>No favorites on this day</p></div>';
        return;
    }

    let html = '';
    let currentDay = null;

    performances.forEach((perf, index) => {
        // Add day header when day changes (for "All Days" view)
        if (perf.Date !== currentDay) {
            currentDay = perf.Date;
            html += `
                <div class="schedule-day-header">
                    <h2>${formatDateFull(perf.Date)}</h2>
                </div>
            `;
        }

        // Calculate gap from previous performance (only within same day)
        if (index > 0) {
            const prevPerf = performances[index - 1];
            // Only show gap if same day
            if (prevPerf.Date === perf.Date) {
                const gap = perf.timestamp - prevPerf.timestamp;
                const gapMinutes = Math.round(gap / 60000);
                if (gapMinutes > 90) {
                    const gapHours = Math.floor(gapMinutes / 60);
                    const gapMins = gapMinutes % 60;
                    const gapText = gapHours > 0
                        ? `${gapHours}h ${gapMins > 0 ? gapMins + 'm' : ''} gap`
                        : `${gapMins}m gap`;
                    html += `
                        <div class="timeline-item">
                            <div class="timeline-gap">${gapText}</div>
                        </div>
                    `;
                }
            }
        }

        html += `
            <div class="timeline-item">
                <div class="timeline-card">
                    <div class="timeline-time">${perf.Time}</div>
                    <div class="timeline-artist">${perf.Artist}</div>
                    <div class="timeline-stage">${perf.Stage}</div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

// Utility
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
