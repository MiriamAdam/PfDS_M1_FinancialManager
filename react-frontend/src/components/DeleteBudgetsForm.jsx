import {useEffect, useState} from "react";

export default function DeleteBudgetForm({onSuccess}) {
    const [budgets, setBudgets] = useState([]);
    const [category_name, setCategoryName] = useState({
        category_name: '',
    });

    useEffect(() => {
        fetch('http://localhost:5000/api/budgets')
            .then(res => res.json())
            .then(data => setBudgets(data))
            .catch(err => console.log(err));
    }, []);

    const handleSubmit = async e => {
        e.preventDefault();
        const response = await fetch(`http://localhost:5000/api/budgets/${category_name}`,
            { method: 'DELETE' }
        );
        if (response.ok) {
            setCategoryName('');
            if (onSuccess) {
            onSuccess();
            }
        }
    }

    return (
        <form onSubmit={handleSubmit} className="flex flex-col justify-between space-y-4 p-6 bg-white rounded-lg shadow w-[50%] ">
            <div>
                <label className="block text-sm font-medium text-gray-700">Budget</label>
                <select
                    value={category_name}
                    onChange={e => setCategoryName(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    required
                >
                    <option value="">Choose a budget</option>
                    {budgets.map(budget => (
                        <option key={budget.category_name} value={budget.category_name}>
                            {budget.category_name}
                        </option>
                    ))}
                </select>
            </div>

            <button
                type="submit"
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
            >
                Delete budget
            </button>
        </form>
    )
}