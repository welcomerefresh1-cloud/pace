import DashboardHeader from "./_components/DashboardHeader";
import StatsGrid from "./_components/StatsGrid";
import RecommendedJobs from "./jobs/_components/RecommendedJobs";
import ProfileStrength from "./_components/ProfileStrength";
import QuickActions from "./_components/QuickActions";
import UpcomingEvents from "./events/_components/UpcomingEvents";
import RecentActivity from "./_components/RecentActivity";

export default function AlumniDashboard() {
    return (
        <div className="space-y-6">
            <DashboardHeader />

            <StatsGrid />

            {/* Main Grid */}
            <div className="grid gap-5 lg:grid-cols-3">
                <RecommendedJobs />

                {/* Right Column */}
                <div className="flex flex-col gap-5 h-full">
                    <ProfileStrength />
                    <QuickActions />
                </div>
            </div>

            {/* Bottom Grid */}
            <div className="grid gap-5 lg:grid-cols-2">
                <UpcomingEvents />
                <RecentActivity />
            </div>
        </div>
    );
}
