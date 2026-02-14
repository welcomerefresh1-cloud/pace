import Link from "next/link";

export default function ProfileStrength() {
    return (
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-600 p-5 text-white">
            <div className="absolute -bottom-6 -right-6 h-24 w-24 rounded-full bg-white/10 blur-xl" />

            <div className="relative">
                <div className="flex items-center justify-between">
                    <h3 className="font-bold text-sm">Profile Strength</h3>
                    <span className="rounded-full bg-white/20 backdrop-blur-sm px-2.5 py-0.5 text-xs font-bold">75%</span>
                </div>

                {/* Progress bar */}
                <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/20">
                    <div className="h-full w-3/4 rounded-full bg-white transition-all duration-500" />
                </div>

                <p className="mt-3 text-xs text-emerald-100">
                    Add your work experience to boost your profile visibility.
                </p>

                <Link
                    href="/dashboard/alumni/profile"
                    className="mt-4 inline-flex items-center gap-1.5 rounded-lg bg-white px-3.5 py-2 text-xs font-semibold text-emerald-700 transition-all hover:bg-emerald-50 hover:shadow-md"
                >
                    Complete Profile
                    <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                </Link>
            </div>
        </div>
    );
}
