import useTransactions from "../components/useTransactions.js";
import React, {useEffect, useState} from 'react';
import {categoryIcons} from "../../categoryIcons.js";

export default function Home() {
    const transactions = useTransactions();
    const balance = transactions.reduce((total, transaction) => total + transaction.amount, 0);
    const [chartUrl, setChartUrl] = useState(null);

    useEffect(() => {
        setChartUrl(`http://localhost:5000/api/chart/monthly-summary?t=${Date.now()}`);
    }, []);

    return(

    <div className="ml-10 mr-25 pb-15">
        <h1 className="text-3xl font-semibold pt-4 pb-4">Overview</h1>
        <h2 className="text-xl pt-2 pb-2">Balance:</h2>
        <div className="bg-white w-fit text-xl font-semibold p-2 border-2 border-gray-200 rounded-2xl shadow-lg">{balance.toFixed(2)} €</div>
        {chartUrl && (
            <div className="bg-white pr-10 pt-3 mt-5 rounded-lg shadow-lg">
                <img
                    src={chartUrl}
                    alt="monthly overview"
                    className="w-full max-w-3xl mx-auto"
                    crossOrigin="anonymous"
                />
            </div>
        )}
        <h2 className="text-xl pt-5 pb-5">Latest Transactions:</h2>
        <div className="bg-white pr-10 pt-3 pl-5 border-2 border-gray-200 rounded-2xl shadow-lg">
            <ul >
                {transactions.slice(-10).reverse().map((t, i) =>
               <li key={i} className="flex items-center gap-2 ">
                    <div className="flex items-center gap-2 p-2 justify-start flex-1">
                        {categoryIcons[t.category_name] && (
                            <img
                                src={categoryIcons[t.category_name]}
                                alt={t.category_name}
                                className="size-10"
                            />
                        )}
                        <span>{t.sub_category}</span>
                    </div>
                   <div className="flex">
                        <span>
                            {new Date(t.date).toLocaleDateString('de-DE', {
                                day: 'numeric',
                                month: 'short'
                            })}
                        </span>
                       <span className="font-bold pl-5 w-30 text-right">{t.amount.toFixed(2)} €</span>
                    </div>
                </li>
                )}
            </ul>
        </div>
    </div>
    )
}