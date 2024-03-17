import type { MetaFunction } from "@remix-run/node";
import { json, ClientActionFunctionArgs, useFetcher } from "@remix-run/react";
import { useState } from 'react';
import { apiPost } from "~/services/api";


type ClimatePavimentReqDTO = {
  mode: string;
  precipitation_mm: number[];
  temp_celsius: number[];
  specific_gravity: number;
  plasticity_index: number;
  california_bearing_ratio: number;
  maximum_dry_density: number;
  optimum_moisture_content: number;
  sieves_passing?: number[];
  p200: number;
};

export const meta: MetaFunction = () => {
  return [
    { title: "Climate Pavement" },
    { name: "description", content: "Climate Pavement calculator" },
  ];
};

const MONTHS: string[] = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

const SIEVES_SIZING = ["2\"", "1-1/2\"", "1\"", "3/4\"", "1/2\"", "3/8\"", "No. 4", "No. 10", "No. 40"];

export async function clientAction({ request }: ClientActionFunctionArgs) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData) as any;

  const pres = MONTHS.map((_, i) => {
    const index = `pre${i}`;
    return data[index]
  })

  const ts = MONTHS.map((_, i) => {
    const index = `t${i}`;
    return data[index]
  })

  const sievePassing = SIEVES_SIZING.map((_, i) => {
    const index = `p${i}`;
    return data[index]
  });

  const reqData: ClimatePavimentReqDTO = {
    mode: data.mode,
    precipitation_mm: pres,
    temp_celsius: ts,
    specific_gravity: data.specific_gravity,
    plasticity_index: data.plasticity_index,
    california_bearing_ratio: data.california_bearing_ratio,
    maximum_dry_density: data.maximum_dry_density,
    optimum_moisture_content: data.optimum_moisture_content,
    p200: data.p200,
  }


  if (data.mode === 'thick') {
    reqData.sieves_passing = sievePassing;
  }

  const dataRes = {
    error: false,
    success: false,
    data: {}
  };

  let resData, resJson;
  try {
    resData = await apiPost('/climate-pavement-calculator', reqData);
    resJson = await resData.json();
  } catch (e) {
    dataRes.error = true;
    return json(dataRes);
  }

  dataRes.success = true;
  dataRes.data = resJson;
  return json(dataRes);
}

export default function Route() {
  const fetcher = useFetcher<typeof clientAction>();
  const [mode, setMode] = useState<string>('thin');

  const isError = fetcher?.data?.error;
  const isSuccess = fetcher?.data?.success;
  const formData = fetcher?.data?.data;

  return (
    <div className="flex flex-wrap flex-col gap-10 p-12">
      <section>
        <h1 className="font-thin text-4xl">Climate Pavement Calculator</h1>
      </section>

      <fetcher.Form method="POST" className="flex flex-col gap-4">
        <div className="flex flex-wrap gap-2 flex-col">
          <label className="font-bold">Mode</label>
          <select name="mode" onChange={(e) => {
            setMode(e.target.value);
          }} required className="p-2">
            <option value="thin">Thin</option>
            <option value="thick">Thick</option>
          </select>
        </div>


        <div className="flex flex-wrap flex-col gap-4" >
          <h2 className="font-bold">Precipitation in mm</h2>
          <div className="flex flex-wrap justify-between gap-4">
            {MONTHS.map((month, monthIndex) => {
              return (
                <div key={monthIndex} className="flex flex-col gap-2">
                  <label className="text-sm">{month}</label>
                  <input type="text" name={`pre${monthIndex}`} required className="border-solid border w-full" />
                </div>
              );
            })}
          </div>
        </div>

        <div className="flex flex-wrap flex-col gap-4" >
          <h2 className="font-bold">Temperature in Celsius</h2>
          <div className="flex flex-wrap justify-between gap-4">
            {MONTHS.map((month, monthIndex) => {
              return (
                <div key={monthIndex} className="flex flex-col gap-2">
                  <label className="text-sm">{month}</label>
                  <input type="text" name={`t${monthIndex}`} required className="border-solid border w-full" />
                </div>
              );
            })}
          </div>
        </div>


        <div className="flex flex-wrap flex-col gap-4">
          <h2 className="font-bold">More parameters</h2>
          <div className="flex flex-wrap gap-4">

            <div className="flex flex-col gap-2">
              <label className="text-sm">Specific gravity</label>
              <input type="text" name="specific_gravity" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">Plasticity index</label>
              <input type="text" name="plasticity_index" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">California bearing ratio</label>
              <input type="text" name="california_bearing_ratio" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">Maximum dry density</label>
              <input type="text" name="maximum_dry_density" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">Optimum moisture content</label>
              <input type="text" name="optimum_moisture_content" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">P200</label>
              <input type="text" name="p200" required className="border-solid border w-full" />
            </div>

          </div>

        </div>


        {mode === 'thick' &&
          <div className='flex flex-col'>
            <h2 className="font-bold">Sieves sizing</h2>

            <div className='flex flex-wrap gap-4'>
              {SIEVES_SIZING.map((size, sizeIndex) => {
                return (
                  <div key={sizeIndex} className="flex flex-col gap-2">
                    <label className="text-sm">{size}</label>
                    <input type="text" name={`p${sizeIndex}`} required className="border-solid border w-full" />
                  </div>
                );
              })}
            </div>
          </div>
        }


        <input className="bg-slate-300 p-2 hover:bg-slate-800 hover:text-slate-200 duration-300 ease cursor-pointer" type="submit" value="Calculate" />
      </fetcher.Form>


      {isError && <span>There is an error.</span>}

      {isSuccess && formData && Object.keys(formData).map((key, keyIndex) => {
        return (
          <div className="flex flex-col gap-4">
            <h3>{key.toUpperCase()}</h3>
            <div className="flex flex-wrap flex justify-between">
              {MONTHS.map((month, monthIndex) => {
                return (
                  <div key={monthIndex} className="flex flex-wrap flex-col gap-2">
                    <span className="text-sm">{month}</span>
                    <span>{parseFloat(formData[key][monthIndex]).toFixed(3)}</span>
                  </div>
                );
              })}

            </div>
          </div>
        );
      })}
    </div>
  );
}
