'use server'

export async function sendQuery(question: String) {

  const resp = await fetch('http://127.0.0.1:3000/api/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question: question })
  });

  const results = await resp.json();
  return results;
}