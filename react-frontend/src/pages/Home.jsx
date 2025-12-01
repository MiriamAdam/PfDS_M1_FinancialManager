import useTransactions from "../components/useTransactions.js";
import React from 'react';
import {categoryIcons} from "../../categoryIcons.js";

export default function Home() {
    const transactions = useTransactions();
    const balance = transactions.reduce((total, transaction) => total + transaction.amount, 0);

    return(

    <div>
        <h1 className="text-3xl font-semibold pt-4 pb-4">Overview</h1>
        <h2 className="text-xl pt-2 pb-2">Balance</h2>
            <div className="text-xl font-semibold p-2">{balance.toFixed(2)} €</div>
        <h2 className="text-xl pt-5">Latest Transactions:</h2>
        <div className="pr-50 pt-3">
            <ul >
                {transactions.slice(-10).map((t, i) =>
               <li key={i} className="flex items-center gap-2 justify-between">
                    <div className="flex items-center gap-2 p-2">
                        {categoryIcons[t.category_name] && (
                            <img
                                src={categoryIcons[t.category_name]}
                                alt={t.category_name}
                                className="size-10"
                            />
                        )}
                        <span>{t.date}</span>
                    </div>
                    <span>{t.sub_category}</span>
                    <span className="font-bold">{t.amount} €</span>
                </li>
                )}
            </ul>
        </div>
    </div>
    )
}