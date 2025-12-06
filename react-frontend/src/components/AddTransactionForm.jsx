import {useEffect, useState} from "react";

export default function AddTransactionForm({onSuccess}) {
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [subCategories, setSubCategories] = useState([]);
    const [formData, setFormData] = useState({
        category: '',
        sub_category: '',
        amount: ''
    });

    useEffect(() => {
        fetch('http://localhost:5000/api/categories')
            .then(res => res.json())
            .then(data => setCategories(data));
    }, []);

    const handleCategoryChange = (e) => {
        const category = e.target.value;
        setSelectedCategory(category);
        const categoryObj = categories.find(cat => cat.category_name === category);

        setFormData({...formData, category, sub_category: ''});

        setSubCategories(categoryObj ? categoryObj.sub_categories : []);
    };

    const handleSubmit = async e => {
        e.preventDefault();
        const response = await fetch('http://localhost:5000/api/transactions', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData)
        });
        if (response.ok) {
            setFormData({category: '', sub_category: '', amount: ''});
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
                    value={formData.category}
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
                <label className="block text-sm font-medium text-gray-700">Sub-Category</label>
                <select
                    value={formData.sub_category}
                    onChange={(e) => setFormData({...formData, sub_category: e.target.value})}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                    required
                    disabled={!selectedCategory}
                >
                    <option value="">Choose a sub-category</option>
                    {subCategories.map(sub => (
                        <option key={sub} value={sub}>{sub}</option>
                    ))}
                </select>
            </div>

            <div>
                <label className="block text-sm font-medium text-gray-700">Amount (€)</label>
                <input
                    type="number"
                    step="0.01"
                    value={formData.amount}
                    onChange={(e) => {
                        let value = parseFloat(e.target.value);
                        if (formData.category !== "Income" && formData.category !== "Sales") {
                            value = -Math.abs(value);
                        }
                        setFormData({...formData, amount: String(value)})}}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm text-center"
                    required
                />
            </div>

            <button
                type="submit"
                className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
            >
                Add transaction
            </button>
        </form>

    );
}