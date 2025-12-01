import React from 'react';

export default function Layout({children}) {
    return (
        <div className="grid grid-rows-[auto-1fr-auot] grid-cols-[auto-1fr] min-h-screen gap-4">
            <div className="col-span-2" >Header</div>
            <div className="">Menu</div>
            <div className="">{children}</div>
            <div className="col-span-2 ">Footer</div>
        </div>
    )
}