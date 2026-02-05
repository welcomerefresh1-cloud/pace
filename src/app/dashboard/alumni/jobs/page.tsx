"use client";

import { useState, useMemo, useEffect } from "react";
import FilterChip from "@/components/dashboard/alumni/FilterChip";
import JobFilters from "./_components/JobFilters";
import JobList from "./_components/JobList";
import { jobData, dateFilters } from "./_components/constants";

export default function JobListingsPage() {
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
    const [locationSearch, setLocationSearch] = useState("");
    const [selectedExperience, setSelectedExperience] = useState<string[]>([]);
    const [selectedWorkTypes, setSelectedWorkTypes] = useState<string[]>([]);
    const [salaryRange, setSalaryRange] = useState<[number, number]>([15, 100]);
    const [tempSalaryRange, setTempSalaryRange] = useState<[number, number]>([15, 100]);
    const [datePosted, setDatePosted] = useState("anytime");
    const [sortBy, setSortBy] = useState("relevant");
    const [currentPage, setCurrentPage] = useState(1);
    const JOBS_PER_PAGE = 10;

    // Debounce salary range updates to prevent layout shift while dragging
    useEffect(() => {
        const timer = setTimeout(() => {
            setSalaryRange(tempSalaryRange);
        }, 300);
        return () => clearTimeout(timer);
    }, [tempSalaryRange]);

    // Calculate date threshold based on filter
    const getDateThreshold = () => {
        const now = new Date();
        switch (datePosted) {
            case "24h":
                return new Date(now.getTime() - 24 * 60 * 60 * 1000);
            case "week":
                return new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
            case "month":
                return new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
            default:
                return new Date(0);
        }
    };

    // Filter and sort jobs
    const filteredJobs = useMemo(() => {
        const dateThreshold = getDateThreshold();

        let filtered = jobData.filter((job) => {
            const matchesSearch =
                searchQuery === "" ||
                job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                job.company.toLowerCase().includes(searchQuery.toLowerCase());

            const matchesType = selectedTypes.length === 0 || selectedTypes.includes(job.type);
            const matchesLocation = locationSearch === "" || job.location.toLowerCase().includes(locationSearch.toLowerCase());
            const matchesExperience = selectedExperience.length === 0 || selectedExperience.includes(job.experienceLevel);
            const matchesWorkType = selectedWorkTypes.length === 0 || selectedWorkTypes.includes(job.workType);
            const matchesSalary = job.salary >= salaryRange[0] && job.salary <= salaryRange[1];
            const matchesDate = job.postedDate >= dateThreshold;

            return matchesSearch && matchesType && matchesLocation && matchesExperience &&
                matchesWorkType && matchesSalary && matchesDate;
        });

        // Sort jobs
        switch (sortBy) {
            case "newest":
                filtered.sort((a, b) => b.postedDate.getTime() - a.postedDate.getTime());
                break;
            case "salary-desc":
                filtered.sort((a, b) => b.salary - a.salary);
                break;
            case "salary-asc":
                filtered.sort((a, b) => a.salary - b.salary);
                break;
            default:
                // Keep original order for "relevant"
                break;
        }

        return filtered;
    }, [searchQuery, selectedTypes, locationSearch, selectedExperience, selectedWorkTypes, salaryRange, datePosted, sortBy]);

    // Calculate counts for each filter option
    const getFilterCounts = (filterType: string, option: string) => {
        const dateThreshold = getDateThreshold();

        return jobData.filter((job) => {
            const matchesSearch =
                searchQuery === "" ||
                job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                job.company.toLowerCase().includes(searchQuery.toLowerCase());

            const matchesSalary = job.salary >= salaryRange[0] && job.salary <= salaryRange[1];
            const matchesDate = job.postedDate >= dateThreshold;

            // Apply all filters except the current one being counted
            let matches = matchesSearch && matchesSalary && matchesDate;

            if (filterType !== "type") {
                matches = matches && (selectedTypes.length === 0 || selectedTypes.includes(job.type));
            }
            if (filterType !== "location") {
                matches = matches && (locationSearch === "" || job.location.toLowerCase().includes(locationSearch.toLowerCase()));
            }
            if (filterType !== "experience") {
                matches = matches && (selectedExperience.length === 0 || selectedExperience.includes(job.experienceLevel));
            }
            if (filterType !== "workType") {
                matches = matches && (selectedWorkTypes.length === 0 || selectedWorkTypes.includes(job.workType));
            }

            // Check if this job matches the option being counted
            switch (filterType) {
                case "type":
                    return matches && job.type === option;
                case "location":
                    return matches && job.location === option;
                case "experience":
                    return matches && job.experienceLevel === option;
                case "workType":
                    return matches && job.workType === option;
                default:
                    return matches;
            }
        }).length;
    };

    const clearFilters = () => {
        setSearchQuery("");
        setSelectedTypes([]);
        setLocationSearch("");
        setSelectedExperience([]);
        setSelectedWorkTypes([]);
        setSalaryRange([15, 100]);
        setTempSalaryRange([15, 100]);
        setDatePosted("anytime");
        setCurrentPage(1);
    };

    // Reset to page 1 when filters change
    useEffect(() => {
        setCurrentPage(1);
    }, [searchQuery, selectedTypes, locationSearch, selectedExperience, selectedWorkTypes, salaryRange, datePosted]);

    const hasActiveFilters =
        searchQuery ||
        selectedTypes.length > 0 ||
        locationSearch ||
        selectedExperience.length > 0 ||
        selectedWorkTypes.length > 0 ||
        salaryRange[0] !== 15 ||
        salaryRange[1] !== 100 ||
        datePosted !== "anytime";

    const toggleFilter = (filterArray: string[], setFilter: (val: string[]) => void, value: string) => {
        if (filterArray.includes(value)) {
            setFilter(filterArray.filter((item) => item !== value));
        } else {
            setFilter([...filterArray, value]);
        }
    };

    // Format relative time
    const getRelativeTime = (date: Date) => {
        const now = new Date();
        const diffMs = now.getTime() - date.getTime();
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffDays = Math.floor(diffHours / 24);

        if (diffHours < 24) return `${diffHours}h ago`;
        if (diffDays < 7) return `${diffDays}d ago`;
        if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`;
        return `${Math.floor(diffDays / 30)}mo ago`;
    };

    return (
        <div className="relative">
            {/* Decorative background elements */}
            <div className="pointer-events-none absolute inset-0 overflow-hidden">
                <div className="absolute top-1/3 -left-20 h-64 w-64 rounded-full bg-blue-100 opacity-30 blur-3xl" />
                <div className="absolute bottom-20 right-1/4 h-48 w-48 rounded-full bg-violet-100 opacity-30 blur-3xl" />
            </div>

            {/* Page Header */}
            <div className="relative mb-8">
                <h1 className="text-2xl font-bold text-slate-900">Job Listings</h1>
                <p className="mt-1 text-slate-500">Discover opportunities that match your skills and career goals</p>
            </div>

            {/* Active Filter Chips */}
            {hasActiveFilters && (
                <div className="relative mb-6 flex flex-wrap items-center gap-2 rounded-xl bg-slate-50 border border-slate-200 p-4">
                    <span className="text-sm font-medium text-slate-600">Active Filters:</span>

                    {searchQuery && (
                        <FilterChip
                            label="Search"
                            value={searchQuery}
                            onRemove={() => setSearchQuery("")}
                        />
                    )}

                    {selectedTypes.map((type) => (
                        <FilterChip
                            key={type}
                            label="Type"
                            value={type}
                            onRemove={() => toggleFilter(selectedTypes, setSelectedTypes, type)}
                        />
                    ))}

                    {locationSearch && (
                        <FilterChip
                            label="Location"
                            value={locationSearch}
                            onRemove={() => setLocationSearch("")}
                        />
                    )}

                    {selectedExperience.map((exp) => (
                        <FilterChip
                            key={exp}
                            label="Experience"
                            value={exp}
                            onRemove={() => toggleFilter(selectedExperience, setSelectedExperience, exp)}
                        />
                    ))}

                    {selectedWorkTypes.map((workType) => (
                        <FilterChip
                            key={workType}
                            label="Work Type"
                            value={workType}
                            onRemove={() => toggleFilter(selectedWorkTypes, setSelectedWorkTypes, workType)}
                        />
                    ))}

                    {(salaryRange[0] !== 15 || salaryRange[1] !== 100) && (
                        <FilterChip
                            label="Salary"
                            value={`₱${salaryRange[0]}k - ₱${salaryRange[1]}k`}
                            onRemove={() => setSalaryRange([15, 100])}
                        />
                    )}

                    {datePosted !== "anytime" && (
                        <FilterChip
                            label="Posted"
                            value={dateFilters.find((d) => d.value === datePosted)?.label || ""}
                            onRemove={() => setDatePosted("anytime")}
                        />
                    )}

                    <button
                        onClick={clearFilters}
                        className="ml-auto text-sm font-medium text-red-600 hover:text-red-700 underline"
                    >
                        Clear All
                    </button>
                </div>
            )}

            {/* 2-Column Layout */}
            <div className="relative grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column: Job Listings */}
                <div className="lg:col-span-2">
                    <JobList
                        filteredJobs={filteredJobs}
                        totalJobs={jobData.length}
                        totalPages={Math.ceil(filteredJobs.length / JOBS_PER_PAGE)}
                        currentPage={currentPage}
                        setCurrentPage={setCurrentPage}
                        sortBy={sortBy}
                        setSortBy={setSortBy}
                        JOBS_PER_PAGE={JOBS_PER_PAGE}
                        clearFilters={clearFilters}
                        getRelativeTime={getRelativeTime}
                    />
                </div>

                {/* Right Column: Search & Filters */}
                <div className="lg:col-span-1">
                    <JobFilters
                        searchQuery={searchQuery}
                        setSearchQuery={setSearchQuery}
                        locationSearch={locationSearch}
                        setLocationSearch={setLocationSearch}
                        selectedTypes={selectedTypes}
                        setSelectedTypes={setSelectedTypes}
                        selectedWorkTypes={selectedWorkTypes}
                        setSelectedWorkTypes={setSelectedWorkTypes}
                        selectedExperience={selectedExperience}
                        setSelectedExperience={setSelectedExperience}
                        tempSalaryRange={tempSalaryRange}
                        setTempSalaryRange={setTempSalaryRange}
                        datePosted={datePosted}
                        setDatePosted={setDatePosted}
                        getFilterCounts={getFilterCounts}
                    />
                </div>
            </div>
        </div>
    );
}
