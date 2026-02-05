import Link from "next/link";

export default function ProfileStrength() {
    return (
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-emerald-500 via-emerald-600 to-emerald-700 p-6 text-white shadow-xl shadow-emerald-500/20">
            {/* Decorative elements */}
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(255,255,255,0.15),transparent_50%)]" />
            <div className="absolute -bottom-8 -right-8 h-32 w-32 rounded-full bg-white/10 blur-xl" />
            <div className="absolute top-0 right-0 h-20 w-20 rounded-full bg-emerald-400/30 blur-2xl" />

            <div className="relative">
                <div className="flex items-center justify-between">
                    <h3 className="font-bold text-lg">Profile Strength</h3>
                    <span className="rounded-full bg-white/20 backdrop-blur-sm px-3 py-1 text-sm font-bold shadow-sm">75%</span>
                </div>

                {/* Enhanced progress bar */}
                <div className="mt-4 h-3 overflow-hidden rounded-full bg-white/20 backdrop-blur-sm">
                    <div className="h-full w-3/4 rounded-full bg-gradient-to-r from-white via-emerald-200 to-white relative overflow-hidden transition-all duration-500">
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent -translate-x-full animate-[shimmer_2s_infinite]" />
                    </div>
                </div>

                <p className="mt-4 text-sm text-emerald-100/90">
                    Add your work experience to boost your profile visibility.
                </p>

                <Link
                    href="/dashboard/alumni/profile"
                    className="mt-5 inline-flex items-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-semibold text-emerald-700 shadow-lg transition-all hover:bg-emerald-50 hover:shadow-xl hover:-translate-y-0.5"
                >
                    Complete Profile
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                </Link>
            </div>
        </div>
    );
}
