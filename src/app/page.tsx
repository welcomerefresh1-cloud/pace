import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-br from-blue-50 to-indigo-50">
      <div className="text-center space-y-6">
        <h1 className="text-6xl font-black text-slate-900 tracking-tight">
          P.A.C.E.
        </h1>
        <p className="text-xl text-slate-600 max-w-lg mx-auto">
          Pasig Alumni Career & Employability System
        </p>

        <div className="flex gap-4 justify-center mt-8">
          <Link href="/dashboard/student">
            <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700">
              Student Login
            </Button>
          </Link>
          <Link href="/dashboard/admin">
            <Button size="lg" variant="outline" className="border-slate-300">
              Admin Access
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
