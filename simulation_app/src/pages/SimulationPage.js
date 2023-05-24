import React, { useState } from "react";
import { useQuery, useMutation, gql } from '@apollo/client';
import "../Styles.css";


const SIMULATION_TYPES_QUERY = gql`
  query SimulationTypes {
    simulation_types {
      id
      name
    }
  }
`;

const CREATE_SIMULATION_TYPE_MUTATION = gql`
  mutation CreateSimulationType($name: String!, $description: String!) {
    createSimulationType(name: $name, description: $description) {
      ok
      simulation_type {
        id
        name
      }
    }
  }
`;



function SimulationPage() {
    const { loading, error, data } = useQuery(SIMULATION_TYPES_QUERY);
    const [createSimulationType, { data: mutationData }] = useMutation(CREATE_SIMULATION_TYPE_MUTATION);
    const [currentHover, setCurrentHover] = useState(null);
    const [createMode, setCreateMode] = useState(false);
    const [typeName, setTypeName] = useState("");
    const [description, setDescription] = useState("");
  
    const handleNextClick = async () => {
        if (createMode) {
          // call the mutation function
          const response = await createSimulationType({ variables: { name: typeName, description: description }});
          console.log(response.data); // check the response
          // Reset fields and switch mode after successful creation
          setTypeName("");
          setDescription("");
          setCreateMode(false);
        }
      };
        
  return (
    <div className="container">
      <div className="header-title">Simulation Dashboard</div>
      <h1 className="block-hero-header">Ready to create or review your simulation?</h1>

      <div className="button-container">
        <div 
          className={currentHover === "create" ? "button-hover" : "button"}
          onMouseEnter={() => setCurrentHover("create")}
        >
          Create a simulation
        </div>

        <div
          className={currentHover === "review" ? "button-hover" : "button"}
          onMouseEnter={() => setCurrentHover("review")}
        >
          Review a result
        </div>
      </div>

      {currentHover === "create" && <div className="button-info">I am creating a simulation</div>}
      {currentHover === "review" && <div className="button-info">I am reviewing a simulation</div>}
    </div>
  );
}

export default SimulationPage;
