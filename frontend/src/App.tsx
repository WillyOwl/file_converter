import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import FileConverter from './components/FileConverter';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <FileConverter />
    </ThemeProvider>
  );
}

export default App; 