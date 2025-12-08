import React, {useEffect, useState} from "react";

export default function Reports() {
    const [chartUrl, setChartUrl] = useState(null);

    useEffect(() => {
        setChartUrl(`http://localhost:5000/api/chart/bar-chart?t=${Date.now()}`);
    }, []);

    return (
        <>
            {chartUrl && (
            <div className="bg-white pl-5 pt-5 pb-5 pr-10 mt-15 rounded-lg shadow-lg w-[90%]">
                <img
                    key={chartUrl}
                    src={chartUrl}
                    alt="monthly overview"
                    className="w-full max-w-3xl mx-auto"
                    crossOrigin="anonymous"
                />
            </div>
            )}
        </>
    )
}