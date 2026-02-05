import DashboardHeader from "@/components/dashboard/alumni/DashboardHeader";
import StatsGrid from "@/components/dashboard/alumni/StatsGrid";
import RecommendedJobs from "@/components/dashboard/alumni/RecommendedJobs";
import ProfileStrength from "@/components/dashboard/alumni/ProfileStrength";
import QuickActions from "@/components/dashboard/alumni/QuickActions";
import UpcomingEvents from "@/components/dashboard/alumni/UpcomingEvents";
import RecentActivity from "@/components/dashboard/alumni/RecentActivity";

export default function AlumniDashboard() {
    return (
        <div className="relative space-y-8">
            {/* Decorative background elements */}
            <div className="pointer-events-none absolute inset-0 overflow-hidden">
                <div className="absolute top-1/3 -left-20 h-64 w-64 rounded-full bg-blue-100 opacity-30 blur-3xl" />
                <div className="absolute bottom-20 right-1/4 h-48 w-48 rounded-full bg-violet-100 opacity-30 blur-3xl" />
            </div>

            <DashboardHeader />

            <StatsGrid />

            {/* Main Grid */}
            <div className="relative grid gap-6 lg:grid-cols-3">
                <RecommendedJobs />

                {/* Right Column */}
                <div className="flex flex-col gap-6 h-full">
                    <ProfileStrength />
                    <QuickActions />
                </div>
            </div>

            {/* Bottom Grid */}
            <div className="relative grid gap-6 lg:grid-cols-2">
                <UpcomingEvents />
                <RecentActivity />
            </div>
        </div>
    );
}
