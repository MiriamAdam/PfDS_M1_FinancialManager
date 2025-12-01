import { useState, useEffect } from 'react'
import {fetchTransactions} from "../services/api.js";

export default function useTransactions() {
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        fetchTransactions()
            .then(data => {
                console.log(data);
                setTransactions(data)
            })
            .catch(err => console.error(err));
    }, []);

    return transactions;
}