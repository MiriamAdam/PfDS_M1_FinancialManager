import {useEffect, useState} from "react";

export default function AddBudgetForm({onSuccess}) {
    const [categories, setCategories] = useState([]);
    const [formData, setFormData] = useState({
        category_name: '',
        limit: ''
    });

    useEffect(() => {
        fetch('http://localhost:5000/api/categories')
            .then(res => res.json())
            .then(data => {
                const only_expenses = data.filter(
                    cat => cat.category_name !== 'Sales' && cat.category_name !== 'Income');
                setCategories(only_expenses);
            })
            .catch(err => console.log(err));
    }, []);

    const handleCategoryChange = (e) => {
        const category_name = e.target.value;
        setFormData({...formData, category_name, limit: ''});
    }

    const handleSubmit = async e => {
        e.preventDefault();
        const response = await fetch('http://localhost:5000/api/budgets', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });
        if (response.ok) {
            setFormData({category_name: '', limit: ''});
            if (onSuccess) {
            onSuccess();
            }
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4 p-6 bg-white rounded-lg shadow w-[50%] ">
            <div>
                <label className="block text-sm font-medium text-gray-700">Category</label>
                <select
                    value={formData.category_name}
                    onChange={handleCategoryChange}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    required
                >
                    <option value="">Choose a category</option>
                    {categories.map(cat => (
                        <option key={cat.category_name} value={cat.category_name}>
                          {cat.category_name}
                        </option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Limit (€)</label>
                <input
                    type="number"
                    step="0.01"
                    value={formData.limit}
                    onChange={(e) => {
                        let value = parseFloat(e.target.value);
                        setFormData({...formData, limit: String(value)})}}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-center"
                    required
                />
            </div>

            <button
                type="submit"
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
            >
                Add budget
            </button>
        </form>
    )
}