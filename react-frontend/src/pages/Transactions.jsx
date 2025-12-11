import {categoryIcons} from "../config/categoryIcons.js";
import React, {useEffect, useState} from "react";
import AddTransactionForm from "../components/AddTransactionForm.jsx";
import {useTransactions} from "../components/TransactionsContext.jsx";
/**
 * Transaction component.
 *
 * Displays all transactions, offers a filter by category
 * and a form for adding new transactions.
 *
 * - Loads the categories from the backend
 * - Allows transactions to be filtered by category
 * - Displays the icon, subcategory, date, and amount of each transaction
 *
 * @component
 * @returns {JSX.Element} Rendered transactions view
 */
export default function Transactions() {
    const {transactions, reload} = useTransactions();
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState("");

    /**
     * Loads the categories from the backend during the first render.
     */
    useEffect(() => {
        fetch("http://localhost:5000/api/categories")
            .then(r => r.json())
            .then(json => setCategories(json))
            .catch(err => console.error(err));
    }, [])

    /**
     * Handler for changing the selected category.
     * Sets the state `selectedCategory` and reloads the corresponding transactions.
     * @param {React.ChangeEvent<HTMLSelectElement>} e - Change event of select field
     */
    const handleCategoryChange = (e) => {
        const category = e.target.value;
        setSelectedCategory(category);
        reload(category);
    }


    return (
        <div className="ml-10 mr-25 pb-15 flex flex-col items-center">
            <div className="pt-5 pb-3"></div>
            <AddTransactionForm onSuccess={reload}/>
            <div className="flex flex-col items-center bg-white pr-10 mt-5 pt-3 pl-5 border-2 border-gray-200 rounded-2xl shadow-lg w-[50%]">
                <label className="block text-sm font-medium text-gray-700 ">Filter by category</label>
                <select
                    value={selectedCategory}
                    onChange={handleCategoryChange}
                    className="mt-1 mb-5 block w-full rounded-md border-gray-300 shadow-sm"
                >
                    <option value="">All transactions</option>
                    {categories.map(cat => (
                        <option key={cat.category_name} value={cat.category_name}>
                          {cat.category_name}
                        </option>
                    ))}
                </select>
            </div>
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
