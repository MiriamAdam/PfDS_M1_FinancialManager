import {useEffect, useState} from "react";
import AddBudgetForm from "../components/AddBudgetForm.jsx";
import DeleteBudgetForm from "../components/DeleteBudgetsForm.jsx";

export default function Budgets() {
    const [ budgets, setBudgets ] = useState(null);
    const loadBudgets = () => {
        fetch('http://localhost:5000/api/budgets')
            .then(res => res.json())
            .then(data => setBudgets(data))
            .catch(err => console.error(err));
    };

    useEffect(() => {
        loadBudgets();
    }, []);

    function renderBudgetsContent() {
        if (!budgets) return <p className={"p-5 text-xl tracking-wide text-gray-700"}>Loading budgets...</p>;
        if (Object.keys(budgets).length === 0) return <p className={"p-5 text-xl tracking-wide text-gray-700"}> - You have not set any budgets -</p>;
        return (<pre>{JSON.stringify(budgets, null, 2)}</pre>);
    }

    return (
        <div className="ml-[10%] mr-25 pb-15">
            <h1 className="text-3xl font-semibold tracking-wider text-gray-700 pt-15 pb-5 ">Manage your monthly budgets:</h1>
            {renderBudgetsContent()}
            <div className="flex justify-center gap-5 w-full">
                <AddBudgetForm onSuccess={loadBudgets} />
                <DeleteBudgetForm onSuccess={loadBudgets} />
            </div>
        </div>
    )
}