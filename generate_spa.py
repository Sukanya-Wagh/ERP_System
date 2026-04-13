import sys

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Principal Dashboard - Academic Workload System</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --neon-cyan: #00F0FF;
            --neon-pink: #FF00FF;
            --neon-purple: #B026FF;
            --neon-gold: #F59E0B;
            --neon-green: #00FF9D;
            --neon-red: #FF3864;
            --dark-bg: #0A0A0F;
            --card-bg: #121218;
            --card-border: #1E1E2E;
            --text-primary: #E0E0E0;
            --text-muted: #8A8A9D;
            --sidebar-bg: #0F0F1A;
            --sidebar-hover: #1A1A2E;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0A0A0F 0%, #121218 100%);
            font-family: 'Inter', sans-serif;
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Sidebar */
        .sidebar {
            position: fixed; left: 0; top: 0; width: 280px; height: 100vh;
            background: var(--sidebar-bg); border-right: 1px solid var(--card-border);
            z-index: 1000; overflow-y: auto;
        }
        .sidebar-header {
            padding: 20px; border-bottom: 1px solid var(--card-border);
            display: flex; align-items: center; justify-content: space-between;
        }
        .logo { font-family: 'Orbitron', monospace; font-weight: 700; font-size: 1.2rem; color: var(--neon-cyan); display: flex; gap: 12px; align-items: center; }
        .menu-section { margin-bottom: 30px; }
        .menu-title { color: var(--text-muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; padding: 0 20px; margin: 20px 0 10px; }
        .menu-item {
            display: flex; align-items: center; gap: 12px; padding: 12px 20px;
            color: var(--text-primary); text-decoration: none; cursor: pointer;
            border-left: 3px solid transparent; transition: all 0.3s;
        }
        .menu-item:hover { background: var(--sidebar-hover); color: var(--neon-cyan); border-left-color: var(--neon-cyan); }
        .menu-item.active { background: rgba(0, 240, 255, 0.1); color: var(--neon-cyan); border-left-color: var(--neon-cyan); }
        
        /* Main Content */
        .main-content { margin-left: 280px; min-height: 100vh; }
        .content-wrapper { padding: 30px; }
        .dashboard-section { display: none; animation: fadeIn 0.3s ease-in-out; }
        .dashboard-section.active { display: block; }
        
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* General Elements */
        .dashboard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .header-left h1 { font-family: 'Orbitron', monospace; font-size: 2rem; font-weight: 700; color: var(--neon-cyan); margin-bottom: 5px; }
        
        /* Stats Grid */
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card {
            background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 25px;
            position: relative; overflow: hidden;
        }
        .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--neon-cyan), transparent); }
        .stat-card.gold::before { background: linear-gradient(90deg, var(--neon-gold), transparent); }
        .stat-card.purple::before { background: linear-gradient(90deg, var(--neon-purple), transparent); }
        .stat-card.red::before { background: linear-gradient(90deg, var(--neon-red), transparent); }
        .stat-icon { width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; margin-bottom: 15px; }
        .stat-icon.cyan { background: rgba(0, 245, 255, 0.1); color: var(--neon-cyan); }
        .stat-icon.gold { background: rgba(245, 158, 11, 0.1); color: var(--neon-gold); }
        .stat-icon.purple { background: rgba(139, 92, 246, 0.1); color: var(--neon-purple); }
        .stat-icon.red { background: rgba(255, 56, 100, 0.1); color: var(--neon-red); }
        .stat-value { font-family: 'Orbitron', monospace; font-size: 1.8rem; font-weight: 700; margin-bottom: 5px; }
        
        .section-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 20px; margin-bottom: 20px; }
        
        /* Tables */
        .data-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        .data-table th { background: rgba(255,255,255,0.02); color: var(--text-muted); font-size: 0.85rem; padding: 12px; text-align: left; text-transform: uppercase; border-bottom: 1px solid var(--card-border); }
        .data-table td { padding: 15px 12px; border-bottom: 1px solid rgba(255,255,255,0.05); color: var(--text-primary); }
        .badge { padding: 5px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }
        .badge-danger { background: rgba(255,56,100,0.1); color: var(--neon-red); border: 1px solid var(--neon-red); }
        .badge-success { background: rgba(0,255,157,0.1); color: var(--neon-green); border: 1px solid var(--neon-green); }
        .badge-warning { background: rgba(245,158,11,0.1); color: var(--neon-gold); border: 1px solid var(--neon-gold); }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header">
            <div class="logo"><i class="fas fa-graduation-cap"></i> Principal Portal</div>
        </div>
        <div class="sidebar-menu">
            <div class="menu-title">Main</div>
            <a class="menu-item active" onclick="switchTab('dashboard')"><i class="fas fa-tachometer-alt"></i> Dashboard Overview</a>
            <a class="menu-item" onclick="switchTab('feedback')"><i class="fas fa-comments"></i> Student Feedback</a>
            <a class="menu-item" onclick="switchTab('workload')"><i class="fas fa-briefcase"></i> Staff Workload (HOD)</a>
            <a class="menu-item" onclick="switchTab('leaves')"><i class="fas fa-calendar-check"></i> Leave Approvals</a>
            <a class="menu-item" onclick="switchTab('notifications')"><i class="fas fa-bell"></i> HOD Notifications</a>
            
            <div class="menu-title">Account</div>
            <a href="{{ url_for('profile') }}" class="menu-item"><i class="fas fa-user"></i> Profile</a>
            <a href="{{ url_for('logout') }}" class="menu-item"><i class="fas fa-sign-out-alt"></i> Logout</a>
        </div>
    </div>

    <div class="main-content">
        <div class="content-wrapper">
            
            <!-- Dashboard Overview Tab -->
            <div id="dashboard" class="dashboard-section active">
                <div class="dashboard-header">
                    <div class="header-left">
                        <h1>Dashboard Overview</h1>
                    </div>
                </div>

                {% if ai_suggestions %}
                <div class="section-card" style="border-left: 4px solid var(--neon-gold)">
                    <h3 style="color:var(--neon-gold); margin-bottom:15px; font-family:'Orbitron', monospace;"><i class="fas fa-robot"></i> AI Suggestions & Alerts</h3>
                    <ul style="list-style:none;">
                    {% for suggestion in ai_suggestions %}
                        <li style="margin-bottom:10px; padding:10px; background:rgba(245,158,11,0.05); border-radius:6px;">{{ suggestion }}</li>
                    {% endfor %}
                    </ul>
                </div>
                {% endif %}

                <div class="stats-grid">
                    <div class="stat-card cyan">
                        <div class="stat-icon cyan"><i class="fas fa-users"></i></div>
                        <div class="stat-value">{{ total_students }}</div>
                        <div class="stat-label">Total Students</div>
                    </div>
                    <div class="stat-card gold">
                        <div class="stat-icon gold"><i class="fas fa-chalkboard-teacher"></i></div>
                        <div class="stat-value">{{ total_faculty }}</div>
                        <div class="stat-label">Total Faculty</div>
                    </div>
                    <div class="stat-card purple">
                        <div class="stat-icon purple"><i class="fas fa-check-double"></i></div>
                        <div class="stat-value">{{ "%.1f"|format(overall_pass_percentage) }}%</div>
                        <div class="stat-label">Avg Pass Rate</div>
                    </div>
                    <div class="stat-card red">
                        <div class="stat-icon red"><i class="fas fa-exclamation-triangle"></i></div>
                        <div class="stat-value">{{ active_issues }}</div>
                        <div class="stat-label">Pending Complaints</div>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="section-card">
                        <h3 style="color:var(--neon-cyan); margin-bottom: 20px;"><i class="fas fa-chart-bar"></i> Workload Distribution</h3>
                        <canvas id="workloadChart" height="200"></canvas>
                    </div>
                    
                    <div class="section-card">
                        <h3 style="color:var(--neon-red); margin-bottom: 20px;"><i class="fas fa-shield-alt"></i> At Risk Students</h3>
                        <div style="max-height:220px; overflow-y:auto;">
                            <table class="data-table">
                                <thead><tr><th>Name</th><th>Risk Factors</th></tr></thead>
                                <tbody>
                                {% for rs in at_risk_students %}
                                    <tr><td>{{ rs.name }}</td><td><span class="badge badge-danger">{{ rs.reasons }}</span></td></tr>
                                {% else %}
                                    <tr><td colspan="2" style="text-align:center;color:var(--neon-green)">No students at risk</td></tr>
                                {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Student Feedback Tab -->
            <div id="feedback" class="dashboard-section">
                <div class="dashboard-header">
                    <div class="header-left">
                        <h1>Student Feedback (Confidential)</h1>
                        <p style="color:var(--text-muted)">All feedback submitted by students for staff members.</p>
                    </div>
                </div>
                <div class="section-card">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Student</th>
                                <th>Target Faculty</th>
                                <th>Subject</th>
                                <th>Satisfaction</th>
                                <th>Comments</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for fb in all_feedback %}
                            <tr>
                                <td>{{ fb.student.full_name or fb.student.username }}</td>
                                <td>{{ fb.faculty.full_name or fb.faculty.username }}</td>
                                <td>{{ fb.subject.name }}</td>
                                <td>
                                    <div style="color:var(--neon-gold)">
                                        {% for i in range(fb.overall_satisfaction) %}<i class="fas fa-star"></i>{% endfor %}
                                        {% for i in range(5 - fb.overall_satisfaction) %}<i class="far fa-star"></i>{% endfor %}
                                    </div>
                                </td>
                                <td>{{ fb.additional_comments or 'No text feedback provided' }}</td>
                                <td>{{ fb.timestamp.strftime('%d-%b-%Y') }}</td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" style="text-align:center;">No feedback available</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Staff Workload Tab -->
            <div id="workload" class="dashboard-section">
                <div class="dashboard-header">
                    <div class="header-left">
                        <h1>HOD Assigned Workload</h1>
                        <p style="color:var(--text-muted)">Detailed breakdown of workload assigned to departmental staff by HODs.</p>
                    </div>
                </div>
                <div class="section-card">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Faculty Name</th>
                                <th>Subject</th>
                                <th>Assigned By (HOD)</th>
                                <th>Hours/Week</th>
                                <th>Assigned On</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for wl in all_workloads %}
                            <tr>
                                <td>{{ wl.faculty.full_name or wl.faculty.username }}</td>
                                <td style="color:var(--neon-cyan)">{{ wl.subject }}</td>
                                <td>{{ wl.hod.full_name or wl.hod.username if wl.hod else 'N/A' }}</td>
                                <td><span class="badge badge-warning">{{ wl.hours }} hrs</span></td>
                                <td>{{ wl.timestamp.strftime('%d-%b-%Y') }}</td>
                            </tr>
                            {% else %}
                            <tr><td colspan="5" style="text-align:center;">No workload assigned yet</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Leaves Tab -->
            <div id="leaves" class="dashboard-section">
                <div class="dashboard-header">
                    <div class="header-left">
                        <h1>Approved Staff Leaves</h1>
                        <p style="color:var(--text-muted)">Showing only leaves of staff that have been approved by HOD.</p>
                    </div>
                </div>
                <div class="section-card">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Staff Member</th>
                                <th>Leave Type</th>
                                <th>Duration</th>
                                <th>Reason</th>
                                <th>Approved By</th>
                                <th>Applied On</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for lv in approved_faculty_leaves %}
                            <tr>
                                <td>{{ lv.user.full_name or lv.user.username }}</td>
                                <td><span class="badge badge-success">{{ lv.leave_type|capitalize }}</span></td>
                                <td>{{ lv.start_date.strftime('%d %b') }} to {{ lv.end_date.strftime('%d %b %Y') }}</td>
                                <td>{{ lv.reason }}</td>
                                <td>{{ lv.approver.full_name or lv.approver.username if lv.approver else 'N/A' }}</td>
                                <td>{{ lv.timestamp.strftime('%d-%b-%Y') }}</td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" style="text-align:center;">No approved staff leaves found</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Notifications Tab -->
            <div id="notifications" class="dashboard-section">
                <div class="dashboard-header">
                    <div class="header-left">
                        <h1>HOD Notifications</h1>
                        <p style="color:var(--text-muted)">Announcements & notices broadcasted by HODs.</p>
                    </div>
                </div>
                <div class="section-card">
                    <div style="display:flex; flex-direction:column; gap:15px;">
                        {% for n in hod_notifications %}
                        <div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:10px; border-left:4px solid var(--neon-purple);">
                            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                                <h4 style="color:var(--neon-purple); font-weight:600;">{{ n.title }}</h4>
                                <span style="color:var(--text-muted); font-size:0.85rem;">{{ n.timestamp.strftime('%d-%b-%Y %H:%M') }}</span>
                            </div>
                            <p style="margin-bottom:10px;">{{ n.content }}</p>
                            <div style="font-size:0.85rem; color:var(--text-muted);">
                                <strong>From:</strong> {{ n.creator.full_name or n.creator.username }} (HOD)
                            </div>
                        </div>
                        {% else %}
                        <div style="text-align:center; padding:20px; color:var(--text-muted);">No HOD notifications found.</div>
                        {% endfor %}
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Chart.js & SPA Logic -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        function switchTab(tabId) {
            // Remove active from links
            document.querySelectorAll('.menu-item').forEach(el => el.classList.remove('active'));
            // Remove active from sections
            document.querySelectorAll('.dashboard-section').forEach(el => el.classList.remove('active'));
            
            // Add active to targeted link & section
            event.currentTarget.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        }

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
                            borderRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#8A8A9D' } },
                            x: { grid: { display: false }, ticks: { color: '#8A8A9D' } }
                        },
                        plugins: { legend: { labels: { color: '#E0E0E0' } } }
                    }
                });
            }
        });
    </script>
</body>
</html>
"""

with open('templates/principal_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("SPA template updated successfully!")
