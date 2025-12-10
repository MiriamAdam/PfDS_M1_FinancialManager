import { createContext, useContext, useState, useEffect } from "react";

const TransactionsContext = createContext();

export function TransactionsProvider({ children }) {
    const [transactions, setTransactions] = useState([]);

    const loadTransactions = (category = null) => {
        let url = "http://localhost:5000/api/transactions";
        if(category){
            url = `${url}?category=${category}`;
        }
        fetch(url)
            .then(res => res.json())
            .then(data => setTransactions([...data]))
            .catch (error => console.error("Error loading transactions", error));
    };

    useEffect(() => {
        loadTransactions();
    }, []);

    return (
        <TransactionsContext.Provider value={{ transactions, reload: loadTransactions }}>
            {children}
        </TransactionsContext.Provider>
    );
}

export function useTransactions() {
    return useContext(TransactionsContext);
}
