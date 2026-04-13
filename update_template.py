import sys

new_main_content = """    <!-- Main Content Area -->
    <div class="main-content">
        <div class="content-wrapper">
            <!-- Header -->
            <div class="dashboard-header" style="margin-bottom: 20px;">
                <div class="header-left">
                    <h1>Principal Dashboard</h1>
                    <div class="breadcrumb">
                        <span>Management & Analytics Overview</span>
                    </div>
                </div>
                <div class="header-right">
                    <div class="search-bar" style="display:flex;gap:10px;">
                        <input type="text" placeholder="Smart Search Students/Faculty..." style="padding:10px;border-radius:8px;background:var(--card-bg);border:1px solid var(--card-border);color:white;width:300px;">
                        <button class="btn btn-primary"><i class="fas fa-search"></i></button>
                    </div>
                    <button class="btn-primary" onclick="window.print()">
                        <i class="fas fa-file-pdf"></i> Download PDF Report
                    </button>
                    <!-- Simulated Excel Download -->
                    <button class="btn-primary" style="background: linear-gradient(135deg, #10b981, #059669);" onclick="alert('Exporting to Excel...')">
                        <i class="fas fa-file-excel"></i> Export Excel
                    </button>
                </div>
            </div>

            <!-- AI Suggestions / Alerts -->
            {% if ai_suggestions %}
            <div class="section-card" style="border-left: 4px solid var(--neon-gold); margin-bottom: 30px;">
                <h3 style="color:var(--neon-gold); margin-bottom:15px; font-family: 'Orbitron', monospace;"><i class="fas fa-robot"></i> AI Management Suggestions & Alerts</h3>
                <ul style="list-style:none; padding-left:0;">
                {% for suggestion in ai_suggestions %}
                    <li style="margin-bottom:10px; padding:15px; background:rgba(245, 158, 11, 0.05); border-radius:8px; border: 1px solid rgba(245, 158, 11, 0.2);">
                        <i class="fas fa-exclamation-circle" style="color:var(--neon-gold); margin-right:10px;"></i>
                        {{ suggestion }}
                    </li>
                {% endfor %}
                </ul>
            </div>
            {% endif %}

            <!-- Overview Stats -->
            <div class="stats-grid">
                <div class="stat-card cyan">
                    <div class="stat-icon cyan"><i class="fas fa-users"></i></div>
                    <div class="stat-value">{{ total_students }}</div>
                    <div class="stat-label">Total Students</div>
                    <div class="stat-sub"><i class="fas fa-arrow-up" style="color:var(--neon-green)"></i> Overall Enrollment</div>
                </div>
                <div class="stat-card gold">
                    <div class="stat-icon gold"><i class="fas fa-chalkboard-teacher"></i></div>
                    <div class="stat-value">{{ total_faculty }}</div>
                    <div class="stat-label">Total Faculty</div>
                    <div class="stat-sub">Active Staff</div>
                </div>
                <div class="stat-card purple">
                    <div class="stat-icon purple"><i class="fas fa-check-double"></i></div>
                    <div class="stat-value">{{ "%.1f"|format(overall_pass_percentage) }}%</div>
                    <div class="stat-label">Avg Pass Rate</div>
                    <div class="stat-sub">Department Wide</div>
                </div>
                <div class="stat-card red">
                    <div class="stat-icon red"><i class="fas fa-exclamation-triangle"></i></div>
                    <div class="stat-value">{{ active_issues }}</div>
                    <div class="stat-label">Pending Complaints</div>
                    <div class="stat-sub">Action Required</div>
                </div>
            </div>

            <!-- Graphs & Charts -->
            <div class="features-grid" style="margin-bottom: 30px; grid-template-columns: 1.5fr 1fr;">
                <div class="feature-card" style="padding:25px;">
                    <h3 style="margin-bottom:20px; font-family: 'Orbitron', monospace; color:var(--text-primary)"><i class="fas fa-chart-line" style="color:var(--neon-cyan); margin-right:10px;"></i> Faculty Workload Distribution</h3>
                    <div style="height: 250px;">
                        <canvas id="workloadChart"></canvas>
                    </div>
                </div>
                <!-- Risk Analysis -->
                <div class="feature-card" style="padding:25px; border-top: 3px solid var(--neon-red);">
                    <h3 style="margin-bottom:20px;color:var(--neon-red); font-family: 'Orbitron', monospace;"><i class="fas fa-user-shield"></i> At-Risk Students List</h3>
                    <div style="max-height: 220px; overflow-y: auto; padding-right: 10px;">
                        <table class="data-table">
                            <thead>
                                <tr><th>Student Name</th><th>Risk Factors</th><th>Actions</th></tr>
                            </thead>
                            <tbody>
                                {% for rs in at_risk_students %}
                                <tr>
                                    <td style="font-weight: 500;">{{ rs.name }}</td>
                                    <td><span style="color:var(--neon-red); font-size:0.85rem; background: rgba(255,0,0,0.1); padding: 4px 8px; border-radius: 4px;">{{ rs.reasons }}</span></td>
                                    <td><button class="btn" style="background:var(--card-border);color:var(--text-primary);padding:5px 10px;font-size:0.8rem; border-radius:4px;"><i class="fas fa-envelope"></i> Notify</button></td>
                                </tr>
                                {% endfor %}
                                {% if not at_risk_students %}
                                <tr><td colspan="3" style="text-align:center; padding:20px; color:var(--neon-green)">No students currently identified at critical risk.</td></tr>
                                {% endif %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Three Column Grid Data -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px;">
                
                <!-- Faculty Performance & Top Students combined -->
                <div class="feature-card" style="padding:25px; border-top: 3px solid var(--neon-green);">
                    <h3 style="margin-bottom:15px;color:var(--neon-green); font-family: 'Orbitron', monospace;"><i class="fas fa-star"></i> Top Performing Students</h3>
                    <ul style="list-style:none; padding-left: 0;">
                    {% for top in top_students %}
                        <li style="padding:12px 10px; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items: center; border-radius: 6px; transition: background 0.2s;">
                            <span style="font-weight: 500;"><i class="fas fa-user-graduate" style="color:var(--text-muted); margin-right:10px;"></i>{{ top.name }}</span>
                            <span style="color:var(--neon-green); font-weight: bold; background: rgba(0,255,157,0.1); padding: 4px 10px; border-radius: 12px;">{{ top.score }}%</span>
                        </li>
                    {% endfor %}
                    </ul>
                </div>

                <!-- Global Announcements & Calendar Preview -->
                <div class="feature-card" style="padding:25px; border-top: 3px solid var(--neon-cyan);">
                    <div style="display:flex; justify-content:space-between; margin-bottom:15px; align-items:center;">
                        <h3 style="font-family: 'Orbitron', monospace;"><i class="fas fa-bullhorn" style="color:var(--neon-cyan)"></i> Announcements</h3>
                        <button class="btn" style="padding:6px 12px; font-size:0.8rem; background:rgba(0, 240, 255, 0.1); color:var(--neon-cyan); border: 1px solid var(--neon-cyan);" onclick="alert('Publishing tool accessed.')"><i class="fas fa-plus"></i> New Notice</button>
                    </div>
                    <ul style="list-style:none; font-size:0.9rem; padding-left: 0;">
                    {% for ann in system_announcements %}
                        <li style="padding:12px 10px; border-bottom:1px solid rgba(255,255,255,0.05);">
                            <div style="color:var(--text-primary); font-weight: bold; margin-bottom:4px;">{{ ann.title }}</div>
                            <div style="color:var(--text-muted); font-size: 0.85rem;">{{ ann.content[:60] }}...</div>
                        </li>
                    {% endfor %}
                    {% if not system_announcements %}
                        <li style="padding:12px 10px; color:var(--text-muted);">No recent announcements.</li>
                    {% endif %}
                    </ul>
                </div>

                <!-- Comprehensive Audit Logs -->
                <div class="feature-card" style="padding:25px; border-top: 3px solid var(--neon-purple);">
                    <h3 style="margin-bottom:15px; font-family: 'Orbitron', monospace;"><i class="fas fa-history" style="color:var(--neon-purple)"></i> System Audit Log (Real-time)</h3>
                    <ul style="list-style:none; font-size:0.85rem; padding-left: 0;">
                    {% for log in recent_logs %}
                        <li style="padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; align-items: flex-start;">
                            <span style="color:var(--neon-cyan); width: 50px; font-weight: bold; font-family: 'Orbitron', monospace;">{{ log.timestamp.strftime('%H:%M') }}</span>
                            <span style="margin-left:10px; color: var(--text-primary); flex: 1;">{{ log.action }}</span>
                        </li>
                    {% endfor %}
                    {% if not recent_logs %}
                        <li style="padding:10px 0; color:var(--text-muted);">No logs recorded.</li>
                    {% endif %}
                    </ul>
                </div>

            </div>
        </div>
    </div>

    <!-- Chart.js and Initialization Script -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            // Setup Workload Chart
            const ctxWorkload = document.getElementById('workloadChart');
            if (ctxWorkload) {
                const wlLabels = JSON.parse('{{ workload_labels | default("[]") | safe }}');
                const wlData = JSON.parse('{{ workload_data | default("[]") | safe }}');
                
                new Chart(ctxWorkload.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: wlLabels,
                        datasets: [{
                            label: 'Assigned Workload (Hours)',
                            data: wlData,
                            backgroundColor: 'rgba(0, 240, 255, 0.2)',
                            borderColor: '#00F0FF',
                            borderWidth: 2,
                            borderRadius: 4,
                            hoverBackgroundColor: 'rgba(0, 240, 255, 0.4)'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: 'rgba(255,255,255,0.05)' },
                                ticks: { color: '#8A8A9D' }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { color: '#8A8A9D' }
                            }
                        },
                        plugins: {
                            legend: { labels: { color: '#E0E0E0' } }
                        }
                    }
                });
            }
        });
    </script>
</body>
</html>
"""

with open('templates/principal_dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for idx, line in enumerate(lines):
    if '<!-- Main Content Area -->' in line:
        break
    new_lines.append(line)

final_content = "".join(new_lines) + new_main_content
with open('templates/principal_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(final_content)
print("Template updated successfully!")
