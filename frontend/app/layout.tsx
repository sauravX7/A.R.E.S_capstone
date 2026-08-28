import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "A.R.E.S. - Autonomous Research & Analysis System",
  description: "AI-powered research and exploratory data analysis platform",
};

import Sidebar from "@/components/Sidebar";

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="h-screen h-full bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 text-white flex overflow-hidden">
        <Sidebar />
        <main className="flex-1 h-full min-h-0 flex flex-col overflow-hidden">
          {children}
        </main>
      </body>
    </html>
  );
}
