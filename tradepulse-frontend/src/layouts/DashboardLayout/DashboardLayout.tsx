import { NavLink, Outlet } from 'react-router-dom';
import './DashboardLayout.css';

const DashboardLayout = () => {
  return (
    <div className="dashboard-layout">
      <aside className="dashboard-layout__sidebar">
        <div className="dashboard-layout__logo">
          Investment Platform
        </div>

        <nav className="dashboard-layout__nav">
          <NavLink to="/dashboard">Dashboard</NavLink>
          <NavLink to="/stocks">Stocks</NavLink>
          <NavLink to="/portfolio">Portfolio</NavLink>
          <NavLink to="/transactions">Transactions</NavLink>
          <NavLink to="/profile">Profile</NavLink>
        </nav>
      </aside>

      <div className="dashboard-layout__main">
        <header className="dashboard-layout__header">
          <h2>Investment Platform</h2>
        </header>

        <main className="dashboard-layout__content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;