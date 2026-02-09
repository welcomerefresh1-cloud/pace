import DashboardHeader from "@/components/dashboard/alumni/DashboardHeader";
import StatsGrid from "@/components/dashboard/alumni/StatsGrid";
import RecommendedJobs from "@/components/dashboard/alumni/RecommendedJobs";
import ProfileStrength from "@/components/dashboard/alumni/ProfileStrength";
import QuickActions from "@/components/dashboard/alumni/QuickActions";
import UpcomingEvents from "@/components/dashboard/alumni/UpcomingEvents";
import RecentActivity from "@/components/dashboard/alumni/RecentActivity";

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
