import { createContext, useContext, useState, useEffect } from "react";

/**
 * Context object for transactions.
 * Provides transaction data and a reload function to update it.
 */
const TransactionsContext = createContext();

/**
 * TransactionsProvider component.
 *
 * Wrap the app (or part of it) with this provider to give access to transaction data
 * and a reload function for fetching transactions from the backend.
 *
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to render within this provider
 * @returns {JSX.Element} TransactionsProvider with context value
 */
export function TransactionsProvider({ children }) {
    const [transactions, setTransactions] = useState([]);

    /**
     * Loads transactions from the backend API.
     * Optionally filters by category or sub-category if provided.
     *
     * @param {string|null} category - Category name to filter transactions (optional)
     * @param {string|null} sub_category - Sub-Category name to filter transactions (optional)
     * @param {string|null} start_date - beginning of date range to filter transactions (optional)
     * @param {string|null} end_date - end of date range to filter transactions (optional)
     */
    const loadTransactions = (category = null, sub_category = null, start_date = null, end_date = null) => {
        let url = "http://localhost:5000/api/transactions";
        const queryParams = [];
        if(sub_category){
            queryParams.push(`sub_category=${sub_category}`)
        }
        else if(category){
            queryParams.push(`category=${category}`)
        }
        if (start_date){
            queryParams.push(`start_date=${start_date}`)
        }
        if (end_date){
            queryParams.push(`end_date=${end_date}`)
        }
        if (queryParams.length > 0) {
        url = `${url}?${queryParams.join('&')}`;
        }
        fetch(url)
            .then(res => res.json())
            .then(data => setTransactions([...data]))
            .catch (error => console.error("Error loading transactions", error));
    };

    /**
     * Load all transactions on component mount.
     */
    useEffect(() => {
        loadTransactions(null, null, null, null);
    }, []);

    return (
        <TransactionsContext.Provider value={{ transactions, reload: loadTransactions }}>
            {children}
        </TransactionsContext.Provider>
    );
}

/**
 * Custom hook to access transaction context.
 * Provides `transactions` state and `reload` function.
 *
 * @returns {{transactions: Array<Object>, reload: function}} Transaction context
 */
export function useTransactions() {
    return useContext(TransactionsContext);
}
