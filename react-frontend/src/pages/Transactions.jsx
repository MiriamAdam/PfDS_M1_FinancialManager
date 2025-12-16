import {categoryIcons} from "../config/categoryIcons.js";
import React, {useEffect, useState} from "react";
import AddTransactionForm from "../components/AddTransactionForm.jsx";
import {useTransactions} from "../components/TransactionsContext.jsx";
/**
 * Transaction component.
 *
 * Displays a form for adding new transactions
 * Shows all transactions and offers to filter by category and sub-category.
 *
 *
 * - Loads the categories from the backend
 * - Allows transactions to be filtered by category and sub-category
 * - Displays the icon, subcategory, date, and amount of each transaction
 *
 * @component
 * @returns {JSX.Element} Rendered transactions view
 */
export default function Transactions() {
    const {transactions, reload} = useTransactions();
    const [categories, setCategories] = useState([]);
    const [subCategories, setSubCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState("");
    const [selectedSubCategory, setSelectedSubCategory] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

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
     * Depending on which category was selected, the SubCategories are set.
     * @param {React.ChangeEvent<HTMLSelectElement>} e - Change event of select field
     */
    const handleCategoryChange = (e) => {
        const category = e.target.value;
        setSelectedCategory(category);
        setSelectedSubCategory("");
        let newSubCategories = []
        if (category) {
            const selectedCat = categories.find(cat => cat.category_name === category);
            newSubCategories = selectedCat ? selectedCat.sub_categories : [];
        }
        setSubCategories(newSubCategories)
        reload(category || null, null, startDate || null, endDate, null);
    }

    const handleSubCategoryChange = (e) => {
        const subCategory = e.target.value;
        setSelectedSubCategory(subCategory)
        if(subCategory){
            reload(null, subCategory, startDate || null, endDate || null);
        } else {
            reload(selectedCategory || null, null, startDate || null, endDate || null);
        }
    }

    const handleDateChange = (isStart, e) => {
        const value = e.target.value;
        let newStartDate = startDate;
        let newEndDate = endDate;

        if (isStart) {
            setStartDate(value);
            newStartDate = value;
        } else {
            setEndDate(value);
            newEndDate = value;
        }
        reload(selectedCategory || null, selectedSubCategory || null, newStartDate || null, newEndDate || null);
    }

    return (
        <div className="ml-10 mr-25 pb-15 flex flex-col items-center">
            <div className="pt-5 pb-3"></div>
            <AddTransactionForm onSuccess={() => reload(selectedCategory || null, selectedSubCategory || null)}/>
            <div className="flex flex-col items-center bg-white pr-10 mt-5 pt-3 pl-5 border-2 border-gray-200 rounded-2xl shadow-lg w-[50%]">
                <label className="block text-sm font-medium text-gray-700 ">Filter by category</label>
                <select
                    value={selectedCategory}
                    onChange={handleCategoryChange}
                    className="mt-1 mb-5 block w-full rounded-md border-gray-300 shadow-sm"
                >
                    <option value="">Choose a category</option>
                    {categories.map(cat => (
                        <option key={cat.category_name} value={cat.category_name}>
                          {cat.category_name}
                        </option>
                    ))}
                </select>
                <select
                    value={selectedSubCategory}
                    onChange={handleSubCategoryChange}
                    className="mt-1 mb-5 block w-full rounded-md border-gray-300 shadow-sm"
                    disabled={!selectedCategory}
                >
                    <option value="">Choose a sub-category</option>
                    {subCategories.map(subCat => (
                        <option key={subCat} value={subCat}>
                          {subCat}
                        </option>
                    ))}
                </select>
            </div>
            <div className="flex flex-col items-center bg-white pr-10 mt-5 pt-3 pl-5 border-2 border-gray-200 rounded-2xl shadow-lg w-[50%]">
                <div className="text-md font-medium text-gray-700 mt-4 mb-2">Filter by date range</div>
                <div className="flex w-full justify-between gap-4 mb-5">
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700">From</label>
                        <input
                            type="date"
                            value={startDate}
                            onChange={(e) => handleDateChange(true, e)}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                        />
                    </div>
                    <div className="flex-1">
                        <label className="block text-sm font-medium text-gray-700">To</label>
                        <input
                            type="date"
                            value={endDate}
                            onChange={(e) => handleDateChange(false, e)}
                            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                        />
                    </div>
                </div>
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
                       <span className={`font-bold pl-5 w-30 text-right ${t.amount < 0 ? 'text-red-600' : 'text-green-600'}`}>{t.amount.toFixed(2)} €</span>
                    </div>
                </li>
                )}
            </ul>
            </div>
        </div>
    )
}
