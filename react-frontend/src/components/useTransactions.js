import { useState, useEffect } from 'react'
import {fetchTransactions} from "../services/api.js";

export default function useTransactions() {
    const [transactions, setTransactions] = useState([]);

    const loadTransactions = () => {
        fetch("http://localhost:5000/api/transactions")
            .then(res => res.json())
            .then(data => setTransactions(data));
    };

    useEffect(() => {
        loadTransactions();
    }, []);

    return { transactions, reload: loadTransactions };
}