import { createContext, useContext, useState, useEffect } from "react";

const TransactionsContext = createContext();

export function TransactionsProvider({ children }) {
    const [transactions, setTransactions] = useState([]);

    const loadTransactions = () => {
        fetch("http://localhost:5000/api/transactions")
            .then(res => res.json())
            .then(data => setTransactions([...data]));
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
