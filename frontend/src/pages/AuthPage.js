import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { RadioGroup, RadioGroupItem } from '../components/ui/radio-group';
import { authAPI } from '../api';
import { useAuth } from '../AuthContext';
import { formatPhone } from '../utils';
import { toast } from 'sonner';

const AuthPage = () => {
  const [step, setStep] = useState('phone'); // phone | otp | register
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [demoOtp, setDemoOtp] = useState('');

  const [formData, setFormData] = useState({
    role: 'CUSTOMER',
    name: '',
    email: '',
    business_name: '',
    brand_shop_name: '',
    gst_number: '',
    gst_registered_name: '',
  });

  const navigate = useNavigate();
  const { login } = useAuth();

  /* =========================
     SEND OTP (FIXED)
     ========================= */
  const handleSendOTP = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formattedPhone = formatPhone(phone);
      const response = await authAPI.sendOTP(formattedPhone);
      const data = response.data;

      if (data?.success) {
        setStep('otp');

        // DEMO MODE SUPPORT
        if (data.otp) {
          setDemoOtp(data.otp);
          toast.success('OTP sent (Demo Mode)');
          console.log('DEMO OTP:', data.otp);
        } else {
          toast.success('OTP sent successfully');
        }
      } else {
        toast.error(data?.message || 'Failed to send OTP');
      }
    } catch (error) {
      // 🔥 CRITICAL FIX: handle demo success even inside catch
      const data = error?.response?.data;

      if (data?.success) {
        setStep('otp');

        if (data.otp) {
          setDemoOtp(data.otp);
          toast.success('OTP sent (Demo Mode)');
          console.log('DEMO OTP:', data.otp);
        }
      } else {
        toast.error(data?.message || 'Failed to send OTP');
      }

      console.error('Send OTP error:', error);
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     VERIFY OTP
     ========================= */
  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formattedPhone = formatPhone(phone);
      const verifyRes = await authAPI.verifyOTP(formattedPhone, otp);

      if (!verifyRes.data.success) {
        toast.error(verifyRes.data.message || 'Invalid OTP');
        return;
      }

      // Try login
      const loginRes = await authAPI.login(formattedPhone);

      if (loginRes.data.success) {
        login(loginRes.data.user, loginRes.data.token);
        toast.success('Login successful');

        if (loginRes.data.user.role === 'ADMIN') {
          navigate('/admin');
        } else {
          navigate('/products');
        }
      } else {
        setStep('register');
      }
    } catch (error) {
      if (
        error.response?.status === 404 ||
        error.response?.data?.message?.includes('not found')
      ) {
        setStep('register');
        toast.info('Please complete registration');
      } else {
        toast.error('OTP verification failed');
      }
      console.error('Verify OTP error:', error);
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     REGISTER
     ========================= */
  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formattedPhone = formatPhone(phone);

      const payload = {
        phone: formattedPhone,
        role: formData.role,
        name: formData.name || null,
        email: formData.email || null,
        business_name: formData.business_name || null,
        brand_shop_name: formData.brand_shop_name || null,
        gst_number: formData.gst_number || null,
        gst_registered_name: formData.gst_registered_name || null,
      };

      const res = await authAPI.register(payload);

      if (res.data.success) {
        login(res.data.user, res.data.token);
        toast.success('Registration successful');

        if (res.data.user.status === 'PENDING') {
          toast.info('Account pending admin approval');
        }

        navigate('/products');
      } else {
        toast.error(res.data.message || 'Registration failed');
      }
    } catch (error) {
      toast.error('Registration failed');
      console.error('Register error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex">
      {/* LEFT */}
      <div
        className="hidden lg:flex lg:w-1/2 bg-cover bg-center relative"
        style={{
          backgroundImage:
            "url('https://images.unsplash.com/photo-1768796373360-95d80c5830fb?q=85')",
        }}
      >
        <div className="absolute inset-0 bg-slate-900/80"></div>
        <div className="relative z-10 p-12 flex flex-col justify-center text-white">
          <h1 className="text-5xl font-black mb-4">CEMENTION</h1>
          <p className="text-slate-200 max-w-md">
            India's trusted B2B cement marketplace.
          </p>
        </div>
      </div>

      {/* RIGHT */}
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-full max-w-md">
          <h2 className="text-3xl font-bold mb-2">
            {step === 'phone' && 'Welcome'}
            {step === 'otp' && 'Verify OTP'}
            {step === 'register' && 'Complete Registration'}
          </h2>

          {/* PHONE */}
          {step === 'phone' && (
            <form onSubmit={handleSendOTP} className="space-y-4">
              <Label>Phone Number</Label>
              <Input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="10-digit mobile number"
                required
              />
              <Button type="submit" disabled={loading} className="w-full">
                {loading ? 'Sending...' : 'Send OTP'}
              </Button>
            </form>
          )}

          {/* OTP */}
          {step === 'otp' && (
            <form onSubmit={handleVerifyOTP} className="space-y-4">
              {demoOtp && (
                <div className="bg-orange-50 p-3 border">
                  <strong>Demo OTP:</strong> {demoOtp}
                </div>
              )}
              <Label>Enter OTP</Label>
              <Input
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                maxLength={6}
                required
              />
              <Button type="submit" disabled={loading} className="w-full">
                Verify OTP
              </Button>
              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={() => setStep('phone')}
              >
                Back
              </Button>
            </form>
          )}

          {/* REGISTER */}
          {step === 'register' && (
            <form onSubmit={handleRegister} className="space-y-4">
              <Label>Select Role</Label>
              <RadioGroup
                value={formData.role}
                onValueChange={(v) =>
                  setFormData({ ...formData, role: v })
                }
              >
                <RadioGroupItem value="CUSTOMER" /> Customer
                <RadioGroupItem value="RETAILER" /> Retailer
                <RadioGroupItem value="DEALER" /> Dealer
              </RadioGroup>

              <Button type="submit" disabled={loading} className="w-full">
                Complete Registration
              </Button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
