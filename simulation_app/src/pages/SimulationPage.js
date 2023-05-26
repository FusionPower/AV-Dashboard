import React, { useState, useEffect } from "react";
import { useQuery, useMutation, gql } from '@apollo/client';
import "../Styles.css";


const SIMULATION_TYPES_QUERY = gql`
  query SimulationTypes {
    simulationTypes {
      id
      name
      description
    }
  }
`;

const CREATE_SIMULATION_TYPE_MUTATION = gql`
  mutation CreateSimulationType($name: String!, $description: String!) {
    createSimulationType(name: $name, description: $description) {
      ok
      simulationType {
        id
        name
        description
      }
    }
  }
`;

const SIMULATION_CONFIGS_QUERY = gql`
  query SimulationConfigs {
    simulationConfigs {
      id
    }
  }
`;

const VEHICLES_QUERY = gql`
  query Vehicles {
    vehicles {
      id
      name
    }
  }
`;

const USER_QUERY = gql`
  query Users {
    users {
      id
    }
  }
`;

const SIMULATION_RESULTS_QUERY = gql`
  query SimulationResults {
    simulationResults {
      id
      success
      navigationData
      safetyMetrics
      vehicleSystemPerformance
    }
  }
`;

const CREATE_SIMULATION_CONFIG = gql`
  mutation CreateSimulationConfig($simulationTypeId: String!, $userId: String!, $vehicleIds: String!, $environmentalConditions: String!, $initialConditions: String!, $physicalConstants: String!, $timeSettings: String!, $trafficRules: String!, $successDefinition: String!) {
    createSimulationConfig(simulationTypeId: $simulationTypeId, userId: $userId, vehicleIds: $vehicleIds, environmentalConditions: $environmentalConditions, initialConditions: $initialConditions, physicalConstants: $physicalConstants, timeSettings: $timeSettings, trafficRules: $trafficRules, successDefinition: $successDefinition) {
      ok
      simulationConfig {
        id
      }
    }
  }
`;

const CREATE_SIMULATION_RESULT = gql`
  mutation CreateSimulationResult($simulationConfigId: String!, $success: String!, $navigationData: String!, $safetyMetrics: String!, $vehicleSystemPerformance: String!) {
    createSimulationResult(simulationConfigId: $simulationConfigId, success: $success, navigationData: $navigationData, safetyMetrics: $safetyMetrics, vehicleSystemPerformance: $vehicleSystemPerformance) {
      ok
      simulationResult {
        id
      }
    }
  }
`;

function SimulationPage() {
    const { loading, error, data } = useQuery(SIMULATION_TYPES_QUERY);
    const [createSimulationType, { data: mutationData }] = useMutation(CREATE_SIMULATION_TYPE_MUTATION);
    const [createSimulationConfig, { data: mutationDataConfig }] = useMutation(CREATE_SIMULATION_CONFIG);
    const [currentHover, setCurrentHover] = useState(null);
    const [createMode, setCreateMode] = useState(false);
    const [typeName, setTypeName] = useState("");
    const [description, setDescription] = useState("");
    const [selectedTypeId, setSelectedTypeId] = useState(1);
    
    

    const [clickCount, setClickCount] = useState(0);

    const { loading: loadingConfig, error: errorConfig, data: dataConfig } = useQuery(SIMULATION_CONFIGS_QUERY);
    const { loading: loadingVehicles, error: errorVehicles, data: dataVehicles } = useQuery(VEHICLES_QUERY);
    const [selectedConfig, setSelectedConfig] = useState(null);
    const [selectedVehicle, setSelectedVehicle] = useState([]);
    const [jsonFields, setJsonFields] = useState({
      environmentalConditions: null,
      initialConditions: null,
      physicalConstants: null,
      timeSettings: null,
      trafficRules: null,
      successDefinition: null,
    });
    useEffect(() => {
      if (dataVehicles && dataVehicles.vehicles && dataVehicles.vehicles.length > 0) {
        setSelectedVehicle([dataVehicles.vehicles[0].id]);
      }
    }, [dataVehicles]);
  
    
    const { loading: loadingUsers, error: errorUsers, data: dataUsers } = useQuery(USER_QUERY);
    const [selectedUserId, setSelectedUserId] = useState(null);

    const [createSimulationResult, { data: mutationResultData }] = useMutation(CREATE_SIMULATION_RESULT);


    const { loading: loadingResults, error: errorResults, data: dataResults } = useQuery(SIMULATION_RESULTS_QUERY);
    const [selectedResultsId, setSelectedResultsId] = useState(null)

    useEffect(() => {
      if (dataUsers && dataUsers.users && dataUsers.users.length > 0) {
        setSelectedUserId(dataUsers.users[0].id);
      }
    }, [dataUsers]);

    useEffect(() => {
      if (dataConfig && dataConfig.simulationConfigs && dataConfig.simulationConfigs.length > 0) {
        setSelectedConfig(dataConfig.simulationConfigs[0].id);
      }
    }, [dataConfig]);
    
    useEffect(() => {
      if (dataResults && dataResults.simulationResults && dataResults.simulationResults.length > 0) {
        setSelectedResultsId(dataResults.simulationResults[0].id);
      }
    }, [dataResults]);
    if (data) {
        console.log(data);
      }
    if (loading) return <p>Loading...</p>;
    if (error) return <p>An error occurred: {error.message}</p>;

    const handleFileUpload = (e, field) => {
      const file = e.target.files[0];
      const reader = new FileReader();
    
      reader.onload = async (e) => {
        const text = (e.target.result);
        try {
          const json = JSON.parse(text);
          setJsonFields(prevState => ({ ...prevState, [field]: json }));
        } catch (err) {
          console.error('Could not parse JSON file: ', err);
        }
      };
    
      reader.onerror = (e) => {
        console.error('Could not read file: ', e);
      };
    
      reader.readAsText(file);
    };
  
    const handleVehicleSelection = (e) => {
      // handle vehicle selection here
    };
  
    const removeSelectedVehicle = (vehicleId) => {
      // remove the selected vehicle from the list
    };

    const submitResult = async () => {
      console.log(selectedConfig);
      const response = await createSimulationResult({ variables: { simulationConfigId: selectedConfig.toString(), success: jsonFields.success, navigationData: jsonFields.navigationData, safetyMetrics: jsonFields.safetyMetrics,  vehicleSystemPerformance: jsonFields.vehicleSystemPerformance}});
      console.log(response.data); 

    };

    const handleNextClick = async () => {
        if (createMode && clickCount === 0) {
            try{
                // call the mutation function
                const response = await createSimulationType({ variables: { name: typeName, description: description }});
                console.log(response.data); // check the response
                // Reset fields and switch mode after successful creation
                setTypeName("");
                setDescription("");
                setCreateMode(false);
                setClickCount(clickCount + 1); 
                setSelectedTypeId(response.data.createSimulationType.simulationType.id);
                console.log(selectedTypeId);
            } catch (e) {
                console.log(e);
            }
        }
        else if (!createMode && clickCount === 0) {
          try{
            setClickCount(clickCount + 1); 
            console.log(dataUsers);
            
          } catch (e) {
              console.log(e);
          }
      }
        else if (clickCount === 1) {
          try{
            // log the types of all the variables
            const vehicleCount = dataVehicles.vehicles.length;
            const response = await createSimulationConfig({ variables: { simulationTypeId: selectedTypeId.toString(), userId: selectedUserId.toString(), vehicleIds: selectedVehicle.toString(), environmentalConditions: jsonFields.environmentalConditions, initialConditions: jsonFields.initialConditions, physicalConstants: jsonFields.physicalConstants, timeSettings: jsonFields.timeSettings, trafficRules: jsonFields.trafficRules, successDefinition: jsonFields.successDefinition }});
            console.log(response.data); // check the response
            setClickCount(clickCount + 1);
          }
          catch (e) {
            console.log(e);
          }
        } 
        else if (clickCount === 2) {
          try{
            // log the types of all the variables
            setClickCount(0);

          }
          catch (e) {
            console.log(e);

          }
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
          className={currentHover === "uploadResult" ? "button-hover" : "button"}
          onMouseEnter={() => setCurrentHover("uploadResult")}
        >
          Review a result
        </div>
        <div
          className={currentHover === "review" ? "button-hover" : "button"}
          onMouseEnter={() => setCurrentHover("review")}
        >
          Review a result
        </div>
      </div>

      {currentHover === "create" && (
        <>
          {clickCount == 0 && createMode ? (
            <>
              <input 
                type="text" 
                placeholder="Simulation type name" 
                value={typeName}
                onChange={e => setTypeName(e.target.value)}
              />
              <textarea 
                placeholder="Description"
                value={description}
                onChange={e => setDescription(e.target.value)}
              />
              <button onClick={() => setCreateMode(false)}>Select Simulation Type</button>
            </>
          ) : clickCount == 0 && !createMode ? (
            <>
                <select  
                    value={selectedTypeId}
                    onChange={(e) => setSelectedTypeId(e.target.value)}
                >
                    {data.simulationTypes.map(type => (
                    <option key={type.id} value={type.id}>{type.name}</option>
                    ))}
                </select>
              <button onClick={() => setCreateMode(true)}>Create Simulation Type</button>
            </>
          ) : clickCount == 1 ? (
            <>
              <div>
                  Simulation Type: {selectedTypeId} {selectedUserId} 1
              </div>
              <div>
                Vehicle:
                <select  
                    value={selectedVehicle}
                    onChange={(e) => setSelectedVehicle(e.target.value)}
                >
                    {dataVehicles.vehicles.map(type => (
                    <option key={type.id} value={type.id}>{type.name}</option>
                    ))}
                </select>
                <div>
                User_id:
                <select  
                  value={selectedUserId}
                    onChange={(e) => setSelectedUserId(e.target.value)}
                >
                    {dataUsers.users.map(type => (
                    <option key={type.id} value={type.id}>{type.id}</option>
                    ))}
                </select>
                </div>
                <div>
                    Environmental Conditions:
                    <input type="file" onChange={(e) => handleFileUpload(e, "environmentalConditions")} />
                  </div>
                  <div>
                    Initial Conditions:
                    <input type="file" onChange={(e) => handleFileUpload(e, "initialConditions")} />
                  </div>
                  <div>
                    Physical Conditions:
                    <input type="file" onChange={(e) => handleFileUpload(e, "physicalConstants")} />
                  </div>
                  <div>
                    Time Settings:
                    <input type="file" onChange={(e) => handleFileUpload(e, "timeSettings")} />
                  </div>
                  <div>
                    Traffic Rules:
                    <input type="file" onChange={(e) => handleFileUpload(e, "trafficRules")} />
                  </div>
                  <div>
                    Success Definition:
                    <input type="file" onChange={(e) => handleFileUpload(e, "successDefinition")} />
                  </div>             
              </div>
              <button onClick={() => setCreateMode(false)}>Select Existing config</button>
            </>
          ) : clickCount == 2 && (
            <>
              <div>
                Simulaiton Created Successfully!
              </div>
            </>
            
          )}
          <button onClick={handleNextClick}>
            {clickCount== 1 ? "Submit" : clickCount==0  ? "Next" : "Create Another Simualtion"}
          </button>
        </>
      )}
      {currentHover === "uploadResult" &&
        <>
            <div>
              Simulation Configuration:
              <select  
                value={selectedConfig}
                  onChange={(e) => setSelectedConfig(e.target.value)}
              >
                  {dataConfig.simulationConfigs.map(type => (
                  <option key={type.id} value={type.id}>{type.id}</option>
                  ))}
              </select>
            </div>
            <div>
              Success:
              <input type="file" onChange={(e) => handleFileUpload(e, "success")} />
            </div>
            <div>
              Navigation Data:
              <input type="file" onChange={(e) => handleFileUpload(e, "navigationData")} />
            </div>
            <div>
              Safety Metrics:
              <input type="file" onChange={(e) => handleFileUpload(e, "safetyMetrics")} />
            </div>
            <div>
              Vehicle System Performance:
              <input type="file" onChange={(e) => handleFileUpload(e, "vehicleSystemPerformance")} />
            </div>

          <div className="button-info">
            <button onClick={submitResult}>
              { "Submit" }
            </button>          
          </div>
        </>
        }
      {currentHover === "review" &&
        <>
        Select a simulation result ID:
        <div className="button-info">
              <select  
                value={selectedResultsId}
                  onChange={(e) => setSelectedResultsId(e.target.value)}
              >
                  {dataResults.simulationResults.map(type => (
                  <option key={type.id} value={type.id}>{type.id}</option>
                  ))}
              </select>        
          </div>
          <div>
            Simulation Config:
            {dataResults.simulationResults[selectedResultsId-1].simulationConfig}
          </div>
          <div>
          Success:
          {dataResults.simulationResults[selectedResultsId-1].navigationData}
          </div>
          <div> 
          Navigation Data:
          {dataResults.simulationResults[selectedResultsId-1].navigationData}
          </div>
          <div>
          Safety Metrics:
          {dataResults.simulationResults[selectedResultsId-1].safetyMetrics}
          </div>
          <div>
          Vehicle System Performance:
          {dataResults.simulationResults[selectedResultsId-1].vehicleSystemPerformance}
          </div>

        </>
        }
    </div>
    
  );
}

export default SimulationPage;
