export default function StudentLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex h-screen w-full">
            <aside className="w-64 bg-indigo-900 text-white p-4">
                {/* Sidebar content to be added */}
                <div className="font-bold text-xl mb-6">PACE Student</div>
                <nav className="space-y-2">
                    <div className="p-2 hover:bg-indigo-800 rounded">Overview</div>
                    <div className="p-2 hover:bg-indigo-800 rounded">Jobs</div>
                    <div className="p-2 hover:bg-indigo-800 rounded">Events</div>
                    <div className="p-2 hover:bg-indigo-800 rounded">Profile</div>
                </nav>
            </aside>
            <main className="flex-1 overflow-auto bg-gray-50">
                {children}
            </main>
        </div>
    );
}
