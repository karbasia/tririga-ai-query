'use client'

import { useEffect, useState } from 'react';

export default function Table({ response } : any) {
  const { query, results } = response;

  const [headers, setHeaders] = useState<any[]>([]);
  const [error, setError] = useState('');

  useEffect(() => {
    if(results && Array.isArray(results)) {
      setError('');
      setHeaders(Object.keys(results[0]));
    } else {
      setError(`Error: ${results.error}`);
    }
  }, [results]);

  return (
    <div className="mb-4">
      <span>Query: {query}</span>
      <div className="text-red-500">{error}</div>
      {error === '' && <div>
        <table className="table-auto">
          <thead>
            <tr>
              {headers.map((header, i) => <th className="p-2" key={i}>{header}</th> )}
            </tr>
          </thead>
          <tbody>
            {Array.isArray(results) && results.map((result: any, i: number) => {
              return (
                <tr key={i}>
                  {headers.map((header, j) => <td className="p-2" key={j}>{Array.isArray(result[header]) ? result[header].join(", ") : result[header]}</td>)}
                </tr>)
            })}
          </tbody>
        </table>
      </div>}
    </div>
  );
}