'use client'

import { useState, FormEvent } from 'react';
import { sendQuery } from '@/app/actions';
import Table from '@/components/table';


export default function Home() {

  const [query, setQuery] = useState('');
  const [responses, setResponses] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const submitQuery = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      const results = await sendQuery(query);
      setResponses(responses => [{query: query, results: results}, ...responses]);
    } finally {
      setQuery('');
      setLoading(false);  
    }
    
  }

  return (
    <div className="h-100 w-full flex items-center justify-center">
      <div className="rounded shadow p-6 m-4 w-full lg:w-3/4">
            <div className="mb-4">
                <h1 className="text-grey-darkest">TRIRIGA AI Data Query</h1>
                <div className="flex mt-4">
                  <form className="flex w-full" onSubmit={submitQuery}>
                    <input 
                      className="shadow appearance-none border rounded w-full py-2 px-3 mr-4" 
                      placeholder="Enter Search Criteria" 
                      value={query}
                      onChange={e => setQuery(e.target.value)}
                    />
                    <button 
                      className="flex-no-shrink p-2 border-2 rounded text-teal border-teal hover:text-white hover:bg-teal"
                      disabled={loading}
                    >Submit</button>
                  </form>
                </div>
            </div>
            <div>
              <div hidden={!loading} className="border-gray-300 h-8 w-8 animate-spin rounded-full border-4 border-r-transparent" />
              {responses.map((response, i) =>
                <Table key={i} response={response}></Table>
              )}
            </div>
        </div>
    </div>
  );
}
