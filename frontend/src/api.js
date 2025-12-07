const BASE_URL = "http://localhost:8000";

export async function apiPost(endpoint, body) {
    const res = await fetch(BASE_URL + endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });

    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Server error");
    }

    return res.json();
}
