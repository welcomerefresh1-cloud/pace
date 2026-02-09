import Link from "next/link";
import EventCard from "./EventCard";

export default function UpcomingEvents() {
    return (
        <div className="rounded-2xl bg-white border border-gray-200/80 p-5 transition-all duration-200 hover:shadow-md">
            <div className="mb-5 flex items-center justify-between">
                <div>
                    <h2 className="text-base font-bold text-gray-900 flex items-center gap-2">
                        <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-violet-50 text-violet-600">
                            <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                        </span>
                        Upcoming Events
                    </h2>
                    <p className="mt-0.5 text-xs text-gray-500">Don&apos;t miss these opportunities</p>
                </div>
                <Link href="/dashboard/alumni/events" className="group text-xs font-medium text-emerald-600 hover:text-emerald-700 flex items-center gap-1 transition-colors">
                    View all
                    <svg className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                </Link>
            </div>
            <div className="space-y-3">
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
