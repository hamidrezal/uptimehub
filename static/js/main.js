
        // ========== STATE ==========
        let autoRefreshInterval;
        let isRefreshing = false;
        let currentFilter = 'all';
        let currentServers = [];

        // ========== DOM Elements ==========
        const serversContainer = document.getElementById('serversContainer');
        const statsContainer = document.getElementById('statsContainer');
        const lastUpdateTimeEl = document.getElementById('lastUpdateTime');
        const refreshIcon = document.getElementById('refreshIcon');

        // ========== توابع رندر (Partial) ==========

        function renderStats(servers) {
            const total = servers.length;
            const up = servers.filter(s => s.status === true).length;
            const down = servers.filter(s => s.status === false).length;
            const uptime = total === 0 ? 0 : Math.round((up / total) * 100);

            statsContainer.innerHTML = `
                <div class="bg-white dark:bg-gray-800 rounded-3xl border border-gray-100 dark:border-gray-700 p-5 shadow-sm">
                    <div class="flex items-center justify-between">
                        <div><p class="text-gray-400 dark:text-gray-500 text-sm">کل سرورها</p><p class="text-3xl font-bold text-gray-800 dark:text-white mt-1">${total}</p></div>
                        <div class="w-12 h-12 bg-blue-50 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center"><i class="fas fa-server text-blue-500 text-xl"></i></div>
                    </div>
                </div>
                <div class="bg-white dark:bg-gray-800 rounded-3xl border border-gray-100 dark:border-gray-700 p-5 shadow-sm">
                    <div class="flex items-center justify-between">
                        <div><p class="text-gray-400 dark:text-gray-500 text-sm">فعال</p><p class="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">${up}</p></div>
                        <div class="w-12 h-12 bg-green-50 dark:bg-green-900/30 rounded-2xl flex items-center justify-center"><i class="fas fa-check-circle text-green-500 text-xl"></i></div>
                    </div>
                </div>
                <div class="bg-white dark:bg-gray-800 rounded-3xl border border-gray-100 dark:border-gray-700 p-5 shadow-sm">
                    <div class="flex items-center justify-between">
                        <div><p class="text-gray-400 dark:text-gray-500 text-sm">غیرفعال</p><p class="text-3xl font-bold text-red-600 dark:text-red-400 mt-1">${down}</p></div>
                        <div class="w-12 h-12 bg-red-50 dark:bg-red-900/30 rounded-2xl flex items-center justify-center"><i class="fas fa-exclamation-circle text-red-500 text-xl"></i></div>
                    </div>
                </div>
                <div class="bg-white dark:bg-gray-800 rounded-3xl border border-gray-100 dark:border-gray-700 p-5 shadow-sm">
                    <div class="flex items-center justify-between">
                        <div><p class="text-gray-400 dark:text-gray-500 text-sm">درآمدیت</p><p class="text-3xl font-bold text-gray-800 dark:text-white mt-1">${uptime}%</p></div>
                        <div class="w-12 h-12 bg-purple-50 dark:bg-purple-900/30 rounded-2xl flex items-center justify-center"><i class="fas fa-chart-line text-purple-500 text-xl"></i></div>
                    </div>
                </div>
            `;

            // آپدیت شمارنده فیلتر
            document.getElementById('filterAllCount').innerHTML = `(${total})`;
            document.getElementById('filterUpCount').innerHTML = `(${up})`;
            document.getElementById('filterDownCount').innerHTML = `(${down})`;
        }

        function renderServersList(servers) {
            if (!servers || servers.length === 0) {
                serversContainer.innerHTML = `
                    <div class="bg-white dark:bg-gray-800 rounded-2xl border border-gray-200 dark:border-gray-700 p-12 text-center">
                        <i class="fas fa-database text-gray-300 dark:text-gray-600 text-5xl mb-4"></i>
                        <h3 class="text-gray-600 dark:text-gray-400 font-medium mb-2">هیچ سروری تنظیم نشده</h3>
                        <a href="/admin/monitor/server/add/" class="inline-flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-2xl text-sm hover:bg-blue-600">➕ افزودن سرور</a>
                    </div>
                `;
                return;
            }

            // مرتب‌سازی
            const sorted = [...servers].sort((a, b) => {
                if (a.status === b.status) return 0;
                return a.status === false ? -1 : 1;
            });

            // فیلتر
            let filtered = sorted;
            if (currentFilter === 'up') filtered = sorted.filter(s => s.status === true);
            if (currentFilter === 'down') filtered = sorted.filter(s => s.status === false);

            if (filtered.length === 0) {
                serversContainer.innerHTML = `<div class="bg-white dark:bg-gray-800 rounded-2xl border p-8 text-center"><p class="text-gray-400">هیچ سروری با این فیلتر نیست</p></div>`;
                return;
            }

            serversContainer.innerHTML = filtered.map(server => `
                <div class="server-card bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 p-4 shadow-sm fade-in">
                    <div class="flex items-center justify-between flex-wrap gap-3">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 rounded-2xl ${server.status ? 'bg-green-50 dark:bg-green-900/30' : 'bg-red-50 dark:bg-red-900/30'} flex items-center justify-center">
                                <i class="fas ${getIcon(server.type)} ${server.status ? 'text-green-500' : 'text-red-500'} text-xl"></i>
                            </div>
                            <div>
                                <div class="flex items-center gap-2 flex-wrap">
                                    <h3 class="font-semibold text-gray-800 dark:text-white">${escapeHtml(server.name)}</h3>
                                    <span class="text-xs text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-0.5 rounded-full">${getTypeLabel(server.type)}</span>
                                </div>
                                <div class="flex items-center gap-3 mt-1 flex-wrap">
                                    <code class="text-xs text-gray-500 font-mono">${escapeHtml(server.address)}${server.port ? `:${server.port}` : ''}</code>
                                    <span class="text-xs text-gray-400"><i class="far fa-clock ml-1"></i>${server.last_check || '---'}</span>
                                </div>
                            </div>
                        </div>
                        <div class="flex items-center gap-2">
                            ${server.status
                                ? '<span class="px-3 py-1 bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs font-medium rounded-full"><i class="fas fa-check-circle ml-1"></i>فعال</span>'
                                : '<span class="px-3 py-1 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-xs font-medium rounded-full"><i class="fas fa-exclamation-circle ml-1"></i>غیرفعال</span>'
                            }
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function getIcon(type) {
            const icons = { 'ping': 'fa-network-wired', 'http': 'fa-globe', 'tcp': 'fa-plug', 'dns': 'fa-dns' };
            return icons[type] || 'fa-server';
        }

        function getTypeLabel(type) {
            const labels = { 'ping': 'پینگ', 'http': 'HTTP', 'tcp': 'TCP', 'dns': 'DNS' };
            return labels[type] || type;
        }

        function escapeHtml(str) { if (!str) return ''; return str.replace(/[&<>]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[m])); }

        // ========== دریافت دیتا با Axios ==========
        async function fetchStatus() {
            if (isRefreshing) return;
            isRefreshing = true;

            try {
                const response = await axios.get('/api/check/', { timeout: 10000 });
                if (response.data.success) {
                    currentServers = response.data.servers;
                    renderStats(currentServers);
                    renderServersList(currentServers);
                    lastUpdateTimeEl.innerText = new Date().toLocaleTimeString('fa-IR');
                }
            } catch (error) {
                console.error('API Error:', error);
                serversContainer.innerHTML = `<div class="bg-white dark:bg-gray-800 rounded-2xl border border-red-200 p-8 text-center"><i class="fas fa-exclamation-triangle text-red-400 text-4xl mb-3"></i><p class="text-gray-600">خطا در ارتباط با سرور</p><button onclick="fetchStatus()" class="mt-3 text-blue-500">تلاش مجدد</button></div>`;
            } finally {
                isRefreshing = false;
            }
        }

        function setFilter(filter) {
            currentFilter = filter;
            document.querySelectorAll('.filter-tab').forEach(tab => tab.classList.remove('active'));
            document.querySelector(`.filter-tab[data-filter="${filter}"]`).classList.add('active');
            renderServersList(currentServers);
        }

        function manualRefresh() {
            refreshIcon.classList.add('fa-spin');
            fetchStatus().finally(() => setTimeout(() => refreshIcon.classList.remove('fa-spin'), 500));
        }

        function startAutoRefresh(seconds = 5) {
            if (autoRefreshInterval) clearInterval(autoRefreshInterval);
            fetchStatus();
            autoRefreshInterval = setInterval(fetchStatus, seconds * 1000);
            document.getElementById('intervalSeconds').innerText = seconds;
        }

        // دارک مود
        function initDarkMode() {
            const isDark = localStorage.getItem('darkMode') === 'true';
            if (isDark) document.documentElement.classList.add('dark');
            document.getElementById('darkModeToggle').addEventListener('click', () => {
                document.documentElement.classList.toggle('dark');
                localStorage.setItem('darkMode', document.documentElement.classList.contains('dark'));
            });
        }

        // Event Listeners
        document.getElementById('refreshBtn').addEventListener('click', manualRefresh);

        // راه‌اندازی
        initDarkMode();
        startAutoRefresh(5);
