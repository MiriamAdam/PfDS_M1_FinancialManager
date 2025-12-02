import React from 'react';

export default function Layout({children}) {
    return (
        <div className="grid grid-rows-[auto_1fr_auto] grid-cols-[auto_1fr] min-h-screen">
            <div className="col-span-2 flex flex-row border-b-2 border-gray-200 text-xl items-center" >
                <img src={'logo.svg'} alt="logo" className="w-25 p-5"/>
                <div className=" ml-5">Phyton for Data Science - 1. Meilenstein</div>
                <div className=" ml-10">Aufgabe 1 – Applikation: Finanzmanager</div>

            </div>
            <nav className="flex flex-col border-r-2 border-gray-200 p-5">
                <a href={'/'} className="flex items-center px-4 py-2 text-gray-700 rounded-md hover:bg-gray-100">Overview</a>
                <a href={'/transactions'} className="flex items-center px-4 py-2 text-gray-700 rounded-md hover:bg-gray-100">Transactions</a>
                <a href={'/reports'} className="flex items-center px-4 py-2 text-gray-700 rounded-md hover:bg-gray-100">Reports</a>
            </nav>
            <div className="bg-blue-50">{children}</div>
            <div className="col-span-2 p-5 border-t-2 border-gray-200 text-base text-center ">bearbeitet von Miriam Adam, Wintersemester 2025/2026, B.Sc. Internationaler Frauenstudiengang Informatik, HS Bremen</div>
        </div>
    )
}