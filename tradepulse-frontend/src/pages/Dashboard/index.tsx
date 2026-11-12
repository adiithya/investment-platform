import {
  Box,
  Card,
  CardContent,
  Chip,
  Grid,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from '@mui/material';

import './Dashboard.css';

const holdings = [
  {
    symbol: 'RELIANCE',
    name: 'Reliance Industries',
    quantity: 20,
    price: 1420,
    value: 28400,
    change: 2.1,
  },
  {
    symbol: 'TCS',
    name: 'Tata Consultancy Services',
    quantity: 10,
    price: 3850,
    value: 38500,
    change: -0.8,
  },
  {
    symbol: 'INFY',
    name: 'Infosys',
    quantity: 15,
    price: 1620,
    value: 24300,
    change: 1.3,
  },
  {
    symbol: 'HDFCBANK',
    name: 'HDFC Bank',
    quantity: 25,
    price: 1750,
    value: 43750,
    change: 0.6,
  },
];

const Dashboard = () => {
  return (
    <Box className="dashboard">
      <Box className="dashboard__header">
        <Typography variant="h4" className="dashboard__title">
          Dashboard
        </Typography>

        <Typography variant="body2" color="text.secondary">
          Welcome back! Here's your investment overview.
        </Typography>
      </Box>

      {/* Portfolio Summary */}
      <Grid container spacing={3} className="dashboard__summary">
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="dashboard__summary-card">
            <CardContent>
              <Typography color="text.secondary" variant="body2">
                Portfolio Value
              </Typography>

              <Typography variant="h5" className="dashboard__value">
                ₹1,35,000
              </Typography>

              <Typography variant="body2" color="success.main">
                +2.45% today
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="dashboard__summary-card">
            <CardContent>
              <Typography color="text.secondary" variant="body2">
                Today's P&L
              </Typography>

              <Typography variant="h5" className="dashboard__value">
                +₹4,250
              </Typography>

              <Typography variant="body2" color="success.main">
                +1.87%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="dashboard__summary-card">
            <CardContent>
              <Typography color="text.secondary" variant="body2">
                Total P&L
              </Typography>

              <Typography variant="h5" className="dashboard__value">
                +₹18,450
              </Typography>

              <Typography variant="body2" color="success.main">
                +15.82%
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <Card className="dashboard__summary-card">
            <CardContent>
              <Typography color="text.secondary" variant="body2">
                Available Balance
              </Typography>

              <Typography variant="h5" className="dashboard__value">
                ₹75,000
              </Typography>

              <Typography variant="body2" color="text.secondary">
                Available to invest
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Holdings */}
      <Box className="dashboard__section">
        <Typography variant="h6" className="dashboard__section-title">
          Your Holdings
        </Typography>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Stock</TableCell>
                <TableCell>Quantity</TableCell>
                <TableCell>Price</TableCell>
                <TableCell>Value</TableCell>
                <TableCell>Change</TableCell>
              </TableRow>
            </TableHead>

            <TableBody>
              {holdings.map((holding) => (
                <TableRow key={holding.symbol} hover>
                  <TableCell>
                    <Stack>
                      <Typography sx={{ fontWeight: 600 }}>
                        {holding.symbol}
                      </Typography>

                      <Typography variant="caption" color="text.secondary">
                        {holding.name}
                      </Typography>
                    </Stack>
                  </TableCell>

                  <TableCell>{holding.quantity}</TableCell>

                  <TableCell>
                    ₹{holding.price.toLocaleString('en-IN')}
                  </TableCell>

                  <TableCell>
                    ₹{holding.value.toLocaleString('en-IN')}
                  </TableCell>

                  <TableCell>
                    <Chip
                      label={`${holding.change > 0 ? '+' : ''}${holding.change}%`}
                      color={holding.change > 0 ? 'success' : 'error'}
                      size="small"
                    />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Box>
  );
};

export default Dashboard;