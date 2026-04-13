# HOD Dashboard - Dark Neon Cyber Theme

A fully functional Head of Department (HOD) Dashboard built with React and Tailwind CSS, featuring a dark neon cyber theme with glassmorphism effects.

## 🚀 Features

### ✨ UI/UX Features
- **Dark Neon Cyber Theme**: Black/dark background with neon cyan, purple, green, yellow accent borders
- **Glassmorphism Cards**: Translucent cards with glowing edges and blur effects
- **Responsive Design**: Optimized for desktop and tablet devices
- **Smooth Animations**: Hover effects, transitions, and glow animations
- **Modern Typography**: Orbitron font for a futuristic look

### 🎯 Functional Features
- **Left Sidebar Navigation**: Collapsible sidebar with 9 main sections
- **Component-based Routing**: Each sidebar item loads corresponding modules
- **Interactive Dashboard**: Working buttons, forms, and data displays
- **Real-time Statistics**: Dynamic stats cards and progress indicators
- **Data Management**: CRUD operations for staff, subjects, and announcements

### 📱 Sidebar Sections
1. **Dashboard** - Overview cards with faculty count, subjects, complaints, announcements
2. **Announcements** - Create/view announcements with priority levels
3. **Manage Staff** - Add, edit, view faculty members with detailed profiles
4. **Subjects** - Subject management with credits, semesters, and assignments
5. **Assign Subjects** - Faculty-subject assignment with workload distribution
6. **Test Marks** - Class test marks management with analytics
7. **Complaints** - View & resolve student complaints with status tracking
8. **Leave Requests** - Approve/reject faculty leave requests
9. **Reports** - Generate downloadable reports with analytics

## 🛠️ Tech Stack

- **Frontend**: React 18.2.0
- **Styling**: Tailwind CSS 3.1.8
- **Icons**: Lucide React 0.263.1
- **Routing**: React Router DOM 6.3.0
- **Build Tool**: Create React App
- **Font**: Google Fonts (Orbitron)

## 📦 Installation

1. **Clone or create the project directory**:
   ```bash
   mkdir hod-dashboard
   cd hod-dashboard
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm start
   ```

4. **Open your browser**:
   Navigate to `http://localhost:3000`

## 🎨 Theme Colors

- **Neon Cyan**: `#00ffff` - Primary accent, dashboard elements
- **Neon Purple**: `#8b5cf6` - Secondary accent, announcements
- **Neon Green**: `#00ff00` - Success states, staff management
- **Neon Yellow**: `#ffff00` - Warnings, subjects, complaints
- **Neon Pink**: `#ff00ff` - Special highlights, assignments
- **Cyber Dark**: `#0a0a0a` - Primary background
- **Cyber Gray**: `#1a1a1a` - Secondary background
- **Cyber Light**: `#2a2a2a` - Elevated surfaces

## 🏗️ Project Structure

```
hod-dashboard/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Dashboard.js          # Main dashboard container
│   │   ├── Sidebar.js           # Navigation sidebar
│   │   ├── Header.js            # Top header with user info
│   │   ├── MainContent.js       # Content area router
│   │   └── sections/            # Individual page components
│   │       ├── DashboardOverview.js
│   │       ├── Announcements.js
│   │       ├── ManageStaff.js
│   │       ├── Subjects.js
│   │       ├── AssignSubjects.js
│   │       ├── TestMarks.js
│   │       ├── Complaints.js
│   │       ├── LeaveRequests.js
│   │       └── Reports.js
│   ├── App.js                   # Root component
│   ├── index.js                 # Entry point
│   └── index.css               # Global styles & animations
├── tailwind.config.js          # Tailwind configuration
├── postcss.config.js           # PostCSS configuration
└── package.json               # Dependencies & scripts
```

## 🎯 Key Components

### Sidebar Navigation
- Collapsible design with icons and labels
- Active state highlighting with neon glow effects
- Mobile-responsive with overlay functionality
- Smooth transitions and hover animations

### Dashboard Overview
- Statistics cards with real-time data
- Action cards for quick access to main functions
- Gradient backgrounds and glassmorphism effects
- Interactive buttons with cyber-style animations

### Data Management Sections
- **Staff Management**: Add/edit faculty with detailed forms
- **Subject Management**: CRUD operations for academic subjects
- **Assignment System**: Faculty-subject mapping with workload tracking
- **Test Marks**: Performance analytics with visual charts
- **Complaints**: Status-based filtering and resolution tracking
- **Leave Requests**: Approval workflow with document support
- **Reports**: Multiple report types with download functionality

## 🎨 Custom Animations

- **Neon Glow**: Pulsing glow effects on active elements
- **Gradient Shift**: Animated gradient text effects
- **Hover Transforms**: Scale and shadow transitions
- **Loading States**: Spinning indicators and progress bars
- **Glassmorphism**: Backdrop blur with transparency

## 📱 Responsive Design

- **Desktop**: Full sidebar with expanded content
- **Tablet**: Collapsible sidebar with optimized layouts
- **Mobile**: Overlay sidebar with touch-friendly interactions

## 🔧 Customization

### Adding New Sections
1. Create a new component in `src/components/sections/`
2. Add the route in `MainContent.js`
3. Add the menu item in `Sidebar.js`
4. Update the header titles in `Header.js`

### Modifying Theme Colors
Update the color palette in `tailwind.config.js`:
```javascript
colors: {
  'neon-cyan': '#00ffff',
  'neon-purple': '#8b5cf6',
  // Add your custom colors
}
```

### Custom Animations
Add new animations in `src/index.css`:
```css
@keyframes your-animation {
  0% { /* start state */ }
  100% { /* end state */ }
}
```

## 🚀 Production Build

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For questions or support, please open an issue in the repository.

---

**Built with ❤️ using React and Tailwind CSS**