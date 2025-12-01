export async function fetchTransactions(category) {
    const url = category
    ? `http://localhost:5000/api/transactions?category=${category}`
        : `http://localhost:5000/api/transactions`

    const resp = await fetch(url)

    if (!resp.ok) {
        throw new Error("Failed to fetch transactions")
    }
    return resp.json()
}