export default function AdminLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex h-screen w-full">
            <aside className="w-64 bg-slate-900 text-white p-4">
                {/* Sidebar content to be added */}
                <div className="font-bold text-xl mb-6">PACE Admin</div>
                <nav className="space-y-2">
                    <div className="p-2 hover:bg-slate-800 rounded">Overview</div>
                    <div className="p-2 hover:bg-slate-800 rounded">Alumni</div>
                    <div className="p-2 hover:bg-slate-800 rounded">Employers</div>
                </nav>
            </aside>
            <main className="flex-1 overflow-auto bg-slate-50">
                {children}
            </main>
        </div>
    );
}
