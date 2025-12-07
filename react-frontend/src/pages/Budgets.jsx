import {useEffect, useState} from "react";
import AddBudgetForm from "../components/AddBudgetForm.jsx";
import DeleteBudgetForm from "../components/DeleteBudgetsForm.jsx";

export default function Budgets() {
    const [ budgets, setBudgets ] = useState(null);
    const loadBudgets = () => {
        fetch('http://localhost:5000/api/budgets')
            .then(res => res.json())
            .then(data => {
                const only_expenses = data.filter(category =>
                category.category_name !== 'Sales' && category.category_name !== 'Income');
                setBudgets(only_expenses);
            })
            .catch(err => console.error(err));
    };

    useEffect(() => {
        loadBudgets();
    }, []);

    function renderBudgetsContent() {
        if (!budgets) return <p>Loading budgets...</p>;
        if (Object.keys(budgets).length === 0) return <p> - You have not set any budgets -</p>;
        return (<pre>{JSON.stringify(budgets, null, 2)}</pre>);
    }

    return (
        <div className="ml-[10%] mr-25 pb-15">
            <h1 className="text-3xl font-semibold tracking-wider text-gray-700 pt-15 pb-5 ">Manage your budgets:</h1>
            {renderBudgetsContent()}
            <div className="flex justify-center gap-5 w-full">
                <AddBudgetForm onSuccess={loadBudgets} />
                <DeleteBudgetForm onSuccess={loadBudgets} />
            </div>
        </div>
    )
}