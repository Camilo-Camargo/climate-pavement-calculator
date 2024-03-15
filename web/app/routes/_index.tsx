import type { MetaFunction } from "@remix-run/node";

export const meta: MetaFunction = () => {
  return [
    { title: "Climate Pavement" },
    { name: "description", content: "Climate Pavement calculator" },
  ];
};

export default function Index() {
  return (
    <div className="font-bold text-2xl">
      <h1>Climate Pavement Calculator</h1>
   </div>
  );
}
