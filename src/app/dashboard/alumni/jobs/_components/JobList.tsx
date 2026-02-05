"use client";

import { ArrowUpDown, TrendingUp, Clock, ArrowDownWideNarrow, ArrowUpWideNarrow } from "lucide-react";
import JobCard from "@/components/dashboard/alumni/JobCard";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";

interface Job {
    id: number;
    title: string;
    company: string;
    location: string;
    salary: number;
    type: string;
    postedDate: Date;
    logo: string;
    experienceLevel: string;
    workType: string;
}

interface JobListProps {
    filteredJobs: Job[];
    totalJobs: number;
    totalPages: number;
    currentPage: number;
    setCurrentPage: (page: number | ((prev: number) => number)) => void;
    sortBy: string;
    setSortBy: (sort: string) => void;
    JOBS_PER_PAGE: number;
    clearFilters: () => void;
    getRelativeTime: (date: Date) => string;
}

export default function JobList({
    filteredJobs,
    totalJobs,
    totalPages,
    currentPage,
    setCurrentPage,
    sortBy,
    setSortBy,
    JOBS_PER_PAGE,
    clearFilters,
    getRelativeTime,
}: JobListProps) {
    const paginatedJobs = filteredJobs.slice(
        (currentPage - 1) * JOBS_PER_PAGE,
        currentPage * JOBS_PER_PAGE
    );

    return (
        <div className="relative rounded-2xl bg-white border border-slate-400/50 p-6 shadow-lg shadow-slate-300/50 hover:shadow-xl transition-all duration-300 overflow-hidden">
            {/* Texture pattern */}
            <div
                className="pointer-events-none absolute inset-0 opacity-[0.015]"
                style={{
                    backgroundImage: `repeating-linear-gradient(
                                    -45deg,
                                    transparent,
                                    transparent 6px,
                                    rgba(0,0,0,0.05) 6px,
                                    rgba(0,0,0,0.05) 7px
                                )`,
                }}
            />
            <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-white to-transparent opacity-80" />
            <div className="absolute -top-10 -right-10 w-40 h-40 bg-gradient-to-br from-emerald-100/50 to-transparent rounded-full blur-2xl" />

            <div className="relative z-10 mb-6 flex items-center justify-between">
                <div>
                    <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                        <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-100 text-blue-600">
                            <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                            </svg>
                        </span>
                        Available Positions
                    </h2>
                    <p className="mt-1 text-sm text-slate-500">
                        Showing <strong className="text-slate-800">{filteredJobs.length}</strong> of {totalJobs} jobs
                    </p>
                </div>

                {/* Sort Dropdown */}
                <Select value={sortBy} onValueChange={setSortBy}>
                    <SelectTrigger className="w-[180px] bg-white border-slate-200 hover:border-emerald-400 transition-colors">
                        <div className="flex items-center gap-2">
                            <ArrowUpDown className="h-4 w-4 text-slate-500" />
                            <SelectValue placeholder="Sort by" />
                        </div>
                    </SelectTrigger>
                    <SelectContent position="popper" align="end" sideOffset={4} className="bg-white">
                        <SelectItem value="relevant">
                            <div className="flex items-center gap-2">
                                <TrendingUp className="h-4 w-4 text-emerald-600" />
                                Most Relevant
                            </div>
                        </SelectItem>
                        <SelectItem value="newest">
                            <div className="flex items-center gap-2">
                                <Clock className="h-4 w-4 text-blue-600" />
                                Newest First
                            </div>
                        </SelectItem>
                        <SelectItem value="salary-desc">
                            <div className="flex items-center gap-2">
                                <ArrowDownWideNarrow className="h-4 w-4 text-amber-600" />
                                Salary: High to Low
                            </div>
                        </SelectItem>
                        <SelectItem value="salary-asc">
                            <div className="flex items-center gap-2">
                                <ArrowUpWideNarrow className="h-4 w-4 text-violet-600" />
                                Salary: Low to High
                            </div>
                        </SelectItem>
                    </SelectContent>
                </Select>
            </div>

            {/* Job Cards List */}
            <div className="relative z-10 flex flex-col gap-4">
                {paginatedJobs.map((job) => (
                    <JobCard
                        key={job.id}
                        title={job.title}
                        company={job.company}
                        location={job.location}
                        salary={`₱${job.salary}k`}
                        type={job.type}
                        postedAgo={getRelativeTime(job.postedDate)}
                        logo={job.logo}
                    />
                ))}
            </div>

            {/* Empty State */}
            {filteredJobs.length === 0 && (
                <div className="relative z-10 py-12 text-center">
                    <div className="flex justify-center mb-4">
                        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-100 text-slate-400">
                            <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </div>
                    </div>
                    <h3 className="text-lg font-semibold text-slate-800 mb-2">No jobs found</h3>
                    <p className="text-slate-500 mb-4">Try adjusting your search or filter criteria</p>
                    <button
                        onClick={clearFilters}
                        className="px-6 py-2.5 rounded-xl bg-emerald-500 text-white font-medium hover:bg-emerald-600 transition-colors"
                    >
                        Clear Filters
                    </button>
                </div>
            )}

            {/* Pagination */}
            {totalPages > 1 && (
                <div className="relative z-10 mt-8 flex items-center justify-center gap-2">
                    {/* Previous Button */}
                    <button
                        onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                        disabled={currentPage === 1}
                        className="flex items-center gap-1 px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-600 font-medium transition-all duration-200 hover:border-emerald-400 hover:text-emerald-600 hover:bg-emerald-50 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-slate-200 disabled:hover:text-slate-600 disabled:hover:bg-slate-50"
                    >
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        Prev
                    </button>

                    {/* Page Numbers */}
                    <div className="flex items-center gap-1">
                        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
                            // Show first, last, current, and adjacent pages
                            const showPage =
                                page === 1 ||
                                page === totalPages ||
                                Math.abs(page - currentPage) <= 1;
                            const showEllipsis =
                                (page === 2 && currentPage > 3) ||
                                (page === totalPages - 1 && currentPage < totalPages - 2);

                            if (!showPage && !showEllipsis) return null;

                            if (showEllipsis && !showPage) {
                                return (
                                    <span key={page} className="px-2 text-slate-400">
                                        ...
                                    </span>
                                );
                            }

                            return (
                                <button
                                    key={page}
                                    onClick={() => setCurrentPage(page)}
                                    className={`min-w-[40px] h-10 rounded-lg font-medium transition-all duration-200 ${currentPage === page
                                        ? "bg-emerald-500 text-white shadow-md shadow-emerald-200"
                                        : "bg-slate-50 border border-slate-200 text-slate-600 hover:border-emerald-400 hover:text-emerald-600 hover:bg-emerald-50"
                                        }`}
                                >
                                    {page}
                                </button>
                            );
                        })}
                    </div>

                    {/* Next Button */}
                    <button
                        onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
                        disabled={currentPage === totalPages}
                        className="flex items-center gap-1 px-4 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-600 font-medium transition-all duration-200 hover:border-emerald-400 hover:text-emerald-600 hover:bg-emerald-50 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:border-slate-200 disabled:hover:text-slate-600 disabled:hover:bg-slate-50"
                    >
                        Next
                        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                    </button>
                </div>
            )}

            {/* Showing X of Y jobs indicator */}
            {filteredJobs.length > 0 && (
                <div className="relative z-10 mt-4 text-center text-sm text-slate-500">
                    Showing {(currentPage - 1) * JOBS_PER_PAGE + 1}-{Math.min(currentPage * JOBS_PER_PAGE, filteredJobs.length)} of {filteredJobs.length} jobs
                </div>
            )}
        </div>
    );
}
