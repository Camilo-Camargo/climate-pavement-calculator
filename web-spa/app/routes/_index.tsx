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
  latitude: number;
  direction: string;
  p200: number;
};


const lang = 'es';

const SPANISH_TEXT = {
  'title': 'Variación de la resistencia de capas de pavimentos por efecto del clima',
  'description': 'Variación de la resistencia de capas de pavimentos por efecto del clima',
  'mode': 'modo',
  'calculate': 'Calcular',
  'direction': 'Dirección',
  'north': 'Norte',
  'south': 'Sur',
  'latitude': 'Latitud',
  'thin': 'Suelos considerados como plásticos (P200 ≥ 10% o wPI ≥ 2.0)',
  'thick': 'Suelos considerados como no Plásticos (P200 < 10% y wPI < 2.0)',
  'precipitation_in_mm': 'Precipitación, P (mm)',
  'temperature_in_celsius': 'Temperatura, T (°C)',
  'more_parameters': 'Caracterización del material',
  'specific_gravity': 'Gravedad específica, Gs ',
  'plasticy_index': 'Índice plástico, IP (%)',
  'california_bearing_ratio': 'Parámetro de resistencia, CBR (%)',
  'maximun_dry_density': 'Densidad seca máxima, γd (kg/m3)',
  'optimum_moisture_content': 'Humedad óptima, ωopt (%)',
  'p200': 'Pasa tamiz No. 200, P200 (%)',
  'sieves_sizing': 'Pasa  en tamices (%)',
  'ept_unadjust': 'Evapotranspiración potencial sin corregir, ETPnc (mm/mes)',
  'ept_adjusted': 'Evapotranspiración potencial corregida, ETP (mm/mes)',
  'tmi': 'Índice de Thornthwaite, TMI',
  'hm': 'Succión matricial, hm (kPa)',
  'ch': 'Factor de ajuste, c(h)',
  'ow': 'Humedad volumétrica, θw',
  's': 'Saturación, S (°/1)',
  'famb': 'Factor ambiental, Famb',
  'cbr': 'CBR afectado por el clima (%)',
  'anual': 'Anual',
  months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
};

const LANG_TEXT = {
  "es": SPANISH_TEXT
};


export const meta: MetaFunction = () => {
  return [
    { title: LANG_TEXT[lang]['title'] },
    { name: "description", content: LANG_TEXT[lang]['description'] },
  ];
};

const SIEVES_SIZING = ["2\"", "1-1/2\"", "1\"", "3/4\"", "1/2\"", "3/8\"", "No. 4", "No. 10", "No. 40"];

export async function clientAction({ request }: ClientActionFunctionArgs) {
  const formData = await request.formData();
  const data = Object.fromEntries(formData) as any;

  const pres = LANG_TEXT[lang].months.map((_, i) => {
    const index = `pre${i}`;
    return data[index]
  })

  const ts = LANG_TEXT[lang].months.map((_, i) => {
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
    latitude: data.latitude,
    direction: data.direction,
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
        <h1 className="font-thin text-4xl">{LANG_TEXT[lang]['title']}</h1>
      </section>

      <fetcher.Form method="POST" className="flex flex-col gap-4">

        <div className="flex flex-wrap gap-2 flex-col">
          <label className="font-bold">{LANG_TEXT[lang]['mode']}</label>
          <select name="mode" onChange={(e) => {
            setMode(e.target.value);
          }} required className="p-2">
            <option value="thin">{LANG_TEXT[lang]['thin']}</option>
            <option value="thick">{LANG_TEXT[lang]['thick']}</option>
          </select>

        </div>

        <div className="flex gap-4">
          <div className="flex gap-2 justify-between items-center">
            <label>{LANG_TEXT[lang]['direction']}</label>
            <select name="direction" onChange={(e) => {
              setMode(e.target.value);
            }} required className="p-2">
              <option value="N">{LANG_TEXT[lang]['north']}</option>
              <option value="S">{LANG_TEXT[lang]['south']}</option>
            </select>
          </div>

          <div className="flex gap-2 justify-between items-center">
            <label>{LANG_TEXT[lang]['latitude']}</label>
            <input type="text" name='latitude' required className="border-solid border" />
          </div>

        </div>


        <div className="flex flex-wrap flex-col gap-4" >
          <h2 className="font-bold">{LANG_TEXT[lang]['precipitation_in_mm']}</h2>
          <div className="flex flex-wrap justify-between gap-4">
            {LANG_TEXT[lang].months.map((month, monthIndex) => {
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
          <h2 className="font-bold">{LANG_TEXT[lang]['temperature_in_celsius']}</h2>
          <div className="flex flex-wrap justify-between gap-4">
            {LANG_TEXT[lang].months.map((month, monthIndex) => {
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
          <h2 className="font-bold">{LANG_TEXT[lang]['more_parameters']}</h2>
          <div className="flex flex-wrap gap-4">

            <div className="flex flex-col gap-2">
              <label className="text-sm">{LANG_TEXT[lang]['specific_gravity']}</label>
              <input type="text" name="specific_gravity" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">{LANG_TEXT[lang]['plasticy_index']}</label>
              <input type="text" name="plasticity_index" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">{LANG_TEXT[lang]['california_bearing_ratio']}</label>
              <input type="text" name="california_bearing_ratio" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">{LANG_TEXT[lang]['maximun_dry_density']}</label>
              <input type="text" name="maximum_dry_density" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">{LANG_TEXT[lang]['optimum_moisture_content']}</label>
              <input type="text" name="optimum_moisture_content" required className="border-solid border w-full" />
            </div>

            <div className="flex flex-col gap-2">
              <label className="text-sm">{LANG_TEXT[lang]['p200']}</label>
              <input type="text" name="p200" required className="border-solid border w-full" />
            </div>

          </div>

        </div>


        {mode === 'thick' &&
          <div className='flex flex-col'>
            <h2 className="font-bold">{LANG_TEXT[lang]['sieves_sizing']}</h2>

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


        <input className="bg-slate-300 p-2 hover:bg-slate-800 hover:text-slate-200 duration-300 ease cursor-pointer" type="submit" value={LANG_TEXT[lang]['calculate']} />
      </fetcher.Form>


      {isError && <span>There is an error.</span>}

      {isSuccess && formData && Object.keys(formData).map((key, keyIndex) => {
        const monthsAndAnual = [...LANG_TEXT[lang].months];
        monthsAndAnual.push(LANG_TEXT[lang].anual);
        return (
          <div className="flex flex-col gap-4">
            <h3>{LANG_TEXT[lang][key]}</h3>
            <div className="flex flex-wrap flex justify-between">
              {monthsAndAnual.map((month, monthIndex) => {
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
