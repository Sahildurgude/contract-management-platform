import { Routes, Route, Link } from "react-router-dom";

import BlueprintList from "./pages/BlueprintList";
import CreateBlueprint from "./pages/CreateBlueprint";
import ContractList from "./pages/ContractList";
import CreateContract from "./pages/CreateContract";

export default function App() {
  return (
    <div>
      {/* Navigation */}
      <nav style={{ padding: 16, borderBottom: "1px solid #ddd" }}>
        <Link to="/blueprints">Blueprints</Link>{" | "}
        <Link to="/blueprints/new">Create Blueprint</Link>{" | "}
        <Link to="/contracts">Contracts</Link>{" | "}
        <Link to="/contracts/new">Create Contract</Link>
      </nav>

      {/* Routes */}
      <Routes>
        {/* Blueprints */}
        <Route path="/" element={<BlueprintList />} />
        <Route path="/blueprints" element={<BlueprintList />} />
        <Route path="/blueprints/new" element={<CreateBlueprint />} />

        {/* Contracts */}
        <Route path="/contracts" element={<ContractList />} />
        <Route path="/contracts/new" element={<CreateContract />} />
       

      </Routes>
    </div>
  );
}
