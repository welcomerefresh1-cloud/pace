import Link from "next/link";
import EventCard from "./EventCard";

export default function UpcomingEvents() {
    return (
        <div className="relative rounded-2xl bg-white border border-slate-400/50 p-6 shadow-lg shadow-slate-300/50 hover:shadow-xl transition-all duration-300 overflow-hidden">
            {/* Subtle texture */}
            <div
                className="pointer-events-none absolute inset-0 opacity-[0.012]"
                style={{
                    backgroundImage: `repeating-linear-gradient(
                        45deg,
                        transparent,
                        transparent 5px,
                        rgba(0,0,0,0.03) 5px,
                        rgba(0,0,0,0.03) 6px
                    )`
                }}
            />
            {/* Top shine */}
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-80" />
            {/* Decorative orb */}
            <div className="absolute -top-8 -left-8 w-32 h-32 bg-gradient-to-br from-violet-100/40 to-transparent rounded-full blur-2xl" />
            <div className="relative z-10 mb-6 flex items-center justify-between">
                <div>
                    <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-violet-100 text-violet-600">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </span>
                        Upcoming Events
                    </h2>
                    <p className="mt-1 text-sm text-slate-500">Don&apos;t miss these opportunities</p>
                </div>
                <Link href="/dashboard/alumni/events" className="group text-sm font-medium text-emerald-600 hover:text-emerald-700 flex items-center gap-1">
                    View all
                    <svg className="h-4 w-4 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                </Link>
            </div>
            <div className="relative z-10 space-y-4">
                <EventCard
                    title="PLP Career Fair 2024"
                    date="15 Feb"
                    time="9:00 AM - 5:00 PM"
                    location="PLP Main Campus"
                    attendees={234}
                    type="Career Fair"
                />
                <EventCard
                    title="Resume Writing Workshop"
                    date="20 Feb"
                    time="2:00 PM - 4:00 PM"
                    location="Virtual Event"
                    attendees={89}
                    type="Workshop"
                />
            </div>
        </div>
    );
}
