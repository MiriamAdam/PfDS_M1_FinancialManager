import useTransactions from "../components/useTransactions.js";

export default function Home() {
    const transactions = useTransactions();
    const balance = transactions.reduce((total, transaction) => total + transaction.amount, 0);

    return(

    <div>
        <h1>Financial Overview</h1>
        <h2>Balance</h2>
        <div>{balance.toFixed(2)} €</div>
        <h2>Transactions</h2>
        <div>
            <ul>
                {transactions.map((t, i) =>
                <li key={i}>
                    {t.date} - {t.category_name}/{t.sub_category}: {t.amount} €
                </li>
                )}
            </ul>
        </div>
    </div>
    )
}