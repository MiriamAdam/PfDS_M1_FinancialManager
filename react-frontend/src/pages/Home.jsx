
import React, {useEffect, useState} from 'react';
import {categoryIcons} from "../config/categoryIcons.js";
import {useTransactions} from "../components/TransactionsContext.jsx";

/**
 * Home component.
 *
 * Displays:
 * - Current account balance
 * - Monthly summary chart
 * - Latest 10 transactions
 *
 * Fetches data from TransactionsContext and updates chart when transactions change.
 *
 * @component
 * @returns {JSX.Element} Rendered Home UI
 */
export default function Home() {
    const { transactions, reload } = useTransactions();
    /**
     * Calculates the total account balance from all transactions.
     * @type {number}
     */
    const balance = transactions.reduce((total, transaction) => total + transaction.amount, 0);
    const [chartUrl, setChartUrl] = useState(null);

    /**
     * Reloads transactions when component mounts.
     */
    useEffect(() => {
      reload();
    }, []);

    /**
     * Updates the monthly summary chart whenever transactions change.
     */
    useEffect(() => {
        setChartUrl(`http://localhost:5000/api/chart/monthly-summary?t=${Date.now()}`);
    }, [transactions]);

    return(

    <div className="ml-[10%] mr-25 pb-15">
        <h1 className="text-3xl font-semibold tracking-wider text-gray-700 pt-15 pb-5 ">Overview</h1>
        <h2 className="text-xl pt-3 pb-3 pl-1 tracking-wide text-gray-700">Balance:</h2>
        <div className="bg-white w-fit text-xl font-semibold p-3 border-2 border-gray-200 rounded-2xl shadow-lg">{balance.toFixed(2)} €</div>
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
        <h2 className="text-xl pl-5 pt-15 pb-5 tracking-wide text-gray-700">Latest Transactions:</h2>
        <div className="bg-white pr-10 pt-3 pl-5 border-2 border-gray-200 rounded-2xl shadow-lg w-[90%]">
            <ul >
                {transactions.slice(0, 10).map((t, i) =>
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