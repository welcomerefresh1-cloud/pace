"use client";

import Link from "next/link";
import JobCard from "./JobCard";
import { useEffect, useState } from "react";
import { JoobleJob, getRecommendedJobs } from "@/app/dashboard/alumni/jobs/_lib/api";
import { Skeleton } from "@/components/ui/skeleton";

const formatSalary = (salaryStr: string) => {
    if (!salaryStr) return "Undisclosed";
    return salaryStr;
};

const formatSnippet = (text: string) => {
    if (!text) return "";
    let snippet = text.replace(/^(\s*\.\.\.\s*)+/, "").trim();
    if (snippet.length > 0) {
        snippet = snippet.charAt(0).toUpperCase() + snippet.slice(1);
    }
    return snippet;
};

export default function RecommendedJobs() {
    const [jobs, setJobs] = useState<JoobleJob[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function fetchRecommended() {
            try {
                const data = await getRecommendedJobs();
                setJobs(data);
            } catch (e) {
                console.error("Failed to fetch recommended jobs", e);
            } finally {
                setIsLoading(false);
            }
        }
        fetchRecommended();
    }, []);

    return (
        <div className="lg:col-span-2 flex flex-col">
            <div className="h-full flex flex-col rounded-2xl bg-white border border-gray-200/80 p-5 transition-all duration-200 hover:shadow-md">
                <div className="mb-5 flex items-center justify-between">
                    <div>
                        <h2 className="text-base font-bold text-gray-900 flex items-center gap-2">
                            <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-amber-50 text-amber-600">
                                <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                                </svg>
                            </span>
                            Recommended For You
                        </h2>
                        <p className="mt-0.5 text-xs text-gray-500">Based on your profile and preferences</p>
                    </div>
                    <Link href="/dashboard/alumni/jobs" className="group text-xs font-medium text-emerald-600 hover:text-emerald-700 flex items-center gap-1 transition-colors">
                        View all
                        <svg className="h-3.5 w-3.5 transition-transform group-hover:translate-x-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </Link>
                </div>
                <div className="flex-1 flex flex-col gap-3">
                    {isLoading ? (
                        <div className="flex flex-col gap-3">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="flex items-start gap-4 p-4 rounded-xl border border-gray-100">
                                    <Skeleton className="h-10 w-10 rounded-lg flex-shrink-0" />
                                    <div className="flex-1 min-w-0">
                                        <div className="flex justify-between items-start mb-2">
                                            <div className="space-y-1.5">
                                                <Skeleton className="h-4 w-48" />
                                                <Skeleton className="h-3.5 w-32" />
                                            </div>
                                            <Skeleton className="h-5 w-20 rounded-full" />
                                        </div>
                                        <div className="space-y-1.5 mb-3">
                                            <Skeleton className="h-3.5 w-full" />
                                            <Skeleton className="h-3.5 w-5/6" />
                                        </div>
                                        <div className="flex gap-4">
                                            <Skeleton className="h-3.5 w-32" />
                                            <Skeleton className="h-3.5 w-24" />
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : jobs.length > 0 ? (
                        jobs.map((job, idx) => (
                            <JobCard
                                key={job.id || idx}
                                title={job.title}
                                company={job.company}
                                location={job.location}
                                salary={formatSalary(job.salary || job.raw_salary || "")}
                                type={job.type || "Full-time"}
                                logo={job.company.charAt(0).toUpperCase()}
                                className="flex-1"
                                description={formatSnippet(job.snippet || job.description || "")}
                            />
                        ))
                    ) : (
                        <div className="flex-1 flex items-center justify-center min-h-[200px] text-sm text-gray-400">
                            No recommendations available at the moment.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
