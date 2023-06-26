import React, { useState, useEffect } from "react";
import { useQuery, useMutation, gql } from '@apollo/client';
import "../Styles.css";
import { Button, Container, Typography, TextField, Select, MenuItem, FormControl, InputLabel, Box } from '@mui/material';
import { styled } from '@mui/system';
import ReactJson from 'react-json-view';


const useStyles = styled((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

const StyledContainer = styled(Container)({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  height: '100vh',
  backgroundColor: '#f5f5f5',
});

const StyledButton = styled(Button)({
  marginTop: '20px',
});


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
      simulationConfigId
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
    const classes = useStyles();

    const { loading, error, data } = useQuery(SIMULATION_TYPES_QUERY);
    const [createSimulationType, { data: mutationData }] = useMutation(CREATE_SIMULATION_TYPE_MUTATION);
    const [createSimulationConfig, { data: mutationDataConfig }] = useMutation(CREATE_SIMULATION_CONFIG);
    const [currentHover, setCurrentHover] = useState(null);
    const [createMode, setCreateMode] = useState(false);
    const [typeName, setTypeName] = useState("");
    const [description, setDescription] = useState("");
    const [selectedTypeId, setSelectedTypeId] = useState(1);
    
    
    const [submitClickCount, setSubmitClickCount] = useState(0);

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
    const [selectedResultsId, setSelectedResultsId] = useState(null);

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
      if (submitClickCount === 0) {
        const response = await createSimulationResult({ variables: { simulationConfigId: selectedConfig.toString(), success: jsonFields.success, navigationData: jsonFields.navigationData, safetyMetrics: jsonFields.safetyMetrics,  vehicleSystemPerformance: jsonFields.vehicleSystemPerformance}});
        console.log(response.data); // check the response
        setSubmitClickCount(submitClickCount + 1);
      }
      if (submitClickCount === 1){
        setSubmitClickCount(0);
      }
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
    <StyledContainer>
      <Typography variant="h2" component="h1">Simulation Dashboard</Typography>
      <Typography variant="h5" component="h2">Ready to create or review your simulation?</Typography>

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
          Upload a result
        </div>
        <div
          className={currentHover === "review" ? "button-hover" : "button"}
          onMouseEnter={() => setCurrentHover("review")}
        >
          Review a result
        </div>
      </div>

      {currentHover === "create" && (
        <Box>
          {clickCount == 0 && createMode ? (
            <Box>
              <TextField
                label="Simulation type name"
                variant="outlined"
                value={typeName}
                onChange={(e) => setTypeName(e.target.value)}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Description"
                multiline
                rows={4}
                variant="outlined"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                fullWidth
                margin="normal"
              />
              <StyledButton onClick={() => setCreateMode(false)}>Select Simulation Type</StyledButton>
            </Box>
          ) : clickCount == 0 && !createMode ? (
            <Box>
              <FormControl fullWidth variant="outlined" margin="normal">
                <InputLabel>Simulation Type</InputLabel>
                <Select
                  value={selectedTypeId}
                  onChange={(e) => setSelectedTypeId(e.target.value)}
                  label="Simulation Type"
                >
                  {data.simulationTypes.map((type) => (
                    <MenuItem key={type.id} value={type.id}>
                      {type.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <StyledButton onClick={() => setCreateMode(true)}>Create Simulation Type</StyledButton>
            </Box>
          ) : clickCount == 1 ? (
            <>
              <Box>
                <Typography variant="h6">
                  Simulation Type: {selectedTypeId}
                </Typography>
                <FormControl fullWidth variant="outlined" margin="normal">
                  <InputLabel>Vehicle</InputLabel>
                  <Select
                    value={selectedVehicle}
                    onChange={(e) => setSelectedVehicle(e.target.value)}
                    label="Vehicle"
                  >
                    {dataVehicles.vehicles.map((type) => (
                      <MenuItem key={type.id} value={type.id}>
                        {type.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl fullWidth variant="outlined" margin="normal">
                  <InputLabel>User ID</InputLabel>
                  <Select
                    value={selectedUserId}
                    onChange={(e) => setSelectedUserId(e.target.value)}
                    label="User ID"
                  >
                    {dataUsers.users.map((type) => (
                      <MenuItem key={type.id} value={type.id}>
                        {type.id}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <Box>
                  <Typography variant="body1">Environmental Conditions:</Typography>
                  <input type="file" onChange={(e) => handleFileUpload(e, "environmentalConditions")} />
                </Box>
                <Box>
                  <Typography variant="body1">Initial Conditions:</Typography>
                  <input type="file" onChange={(e) => handleFileUpload(e, "initialConditions")} />
                </Box>
                <Box>
                  <Typography variant="body1">Physical Conditions:</Typography>
                  <input type="file" onChange={(e) => handleFileUpload(e, "physicalConstants")} />
                </Box>
                <Box>
                  <Typography variant="body1">Time Settings:</Typography>
                  <input type="file" onChange={(e) => handleFileUpload(e, "timeSettings")} />
                </Box>
                <Box>
                  <Typography variant="body1">Traffic Rules:</Typography>
                  <input type="file" onChange={(e) => handleFileUpload(e, "trafficRules")} />
                </Box>
                <Box>
                  <Typography variant="body1">Success Definition:</Typography>
                  <input type="file" onChange={(e) => handleFileUpload(e, "successDefinition")} />
                </Box>
              </Box>
            </>
          ) : clickCount == 2 && (
            <Typography variant="h6" color="success">
              Simulation Created Successfully!
            </Typography>
                
          )}
          <StyledButton onClick={handleNextClick}>
            {clickCount == 1 ? "Submit" : clickCount == 0  ? "Next" : "Create Another Simulation"}
          </StyledButton>
        </Box>
      )}
      {currentHover === "uploadResult" && (
        submitClickCount == 0 ? ( 
          <Box>
            <FormControl fullWidth variant="outlined" margin="normal">
              <InputLabel>Simulation Configuration</InputLabel>
              <Select
                value={selectedConfig}
                onChange={(e) => setSelectedConfig(e.target.value)}
                label="Simulation Configuration"
              >
                {dataConfig.simulationConfigs.map((config) => (
                  <MenuItem key={config.id} value={config.id}>
                    {config.id}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Box>
              <Typography variant="body1">Success:</Typography>
              <input type="file" onChange={(e) => handleFileUpload(e, "success")} />
            </Box>
            <Box>
              <Typography variant="body1">Navigation Data:</Typography>
              <input type="file" onChange={(e) => handleFileUpload(e, "navigationData")} />
            </Box>
            <Box>
              <Typography variant="body1">Safety Metrics:</Typography>
              <input type="file" onChange={(e) => handleFileUpload(e, "safetyMetrics")} />
            </Box>
            <Box>
              <Typography variant="body1">Vehicle System Performance:</Typography>
              <input type="file" onChange={(e) => handleFileUpload(e, "vehicleSystemPerformance")} />
            </Box>
            <Box className="button-info" mt={2}>
              <Button variant="contained" color="primary" onClick={submitResult}>
                Submit
              </Button>
            </Box>
          </Box>        
        ) : submitClickCount == 1 && (
          <Box>
            <Typography variant="body1">Simulation created successfully</Typography>
            <Box className="button-info" mt={2}>
              <Button variant="contained" color="primary" onClick={submitResult}>
                Create a new simulation
              </Button>
            </Box>
          </Box>
        )
      )}
      {currentHover === "review" &&
        <Box>
        <Typography variant="h6">Select a simulation result ID:</Typography>
        <Box className="button-info" marginY={2}>
          <FormControl fullWidth variant="outlined" margin="normal">
            <InputLabel id="simulation-result-id-label">Simulation Result ID</InputLabel>
            <Select
              labelId="simulation-result-id-label"
              value={selectedResultsId}
              onChange={(e) => setSelectedResultsId(e.target.value)}
              label="Simulation Result ID"  // Added label prop
            >
              {dataResults.simulationResults.map(result => (
                <MenuItem key={result.id} value={result.id}>
                  {result.id}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
        
        <Typography variant="body1">
          <strong>Simulation Config:</strong>
          {dataResults.simulationResults[selectedResultsId-1].simulationConfigId}
        </Typography>
        <Typography variant="body1">
          <strong>Success:</strong>
          {dataResults.simulationResults[selectedResultsId-1].navigationData}
        </Typography>
        <Typography variant="body1">
          <strong>Navigation Data:</strong>
          {dataResults.simulationResults[selectedResultsId-1].navigationData}
        </Typography>
        <Typography variant="body1">
          <strong>Safety Metrics:</strong>
          {dataResults.simulationResults[selectedResultsId-1].safetyMetrics}
        </Typography>
        <Typography variant="body1">
          <strong>Vehicle System Performance:</strong>
          {dataResults.simulationResults[selectedResultsId-1].vehicleSystemPerformance}
        </Typography>
      </Box>    
  }
    </StyledContainer>
    
  );
}

export default SimulationPage;
