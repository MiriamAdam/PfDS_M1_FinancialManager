import {categoryIcons} from "../../categoryIcons.js";
import React from "react";
import AddTransactionForm from "../components/AddTransactionForm.jsx";
import {useTransactions} from "../components/TransactionsContext.jsx";

export default function Transactions() {
    const {transactions, reload} = useTransactions();

    return (
        <div className="ml-10 mr-25 pb-15 flex flex-col items-center">
            <div className="pt-5 pb-3"></div>
            <AddTransactionForm onSuccess={reload}/>
            <div className="bg-white pr-10 mt-5 pt-3 pl-5 border-2 border-gray-200 rounded-2xl shadow-lg max-h-200 overflow-y-auto w-[50%]">
            <ul >
                {transactions.map((t, i) =>
               <li key={i} className="flex items-center gap-2 ">
                    <div className="flex items-center gap-2 p-2 justify-start flex-1">
                        {categoryIcons[t.category_name] && (
                            <img
                                src={categoryIcons[t.category_name]}
                                alt={t.category_name}
                                className="size-10 mr-3"
                            />
                        )}
                        <span>{t.sub_category}</span>
                    </div>
                   <div className="flex">
                        <span>
                            {new Date(t.date).toLocaleDateString('de-DE', {
                                day: 'numeric',
                                month: 'long',
                                year: 'numeric'
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