// HARFANG(R) Copyright (C) 2022 NWNC. Released under GPL/LGPL/Commercial Licence, see licence.txt for details.

#pragma once

#include "foundation/math.h"

#if defined(__cpluscplus)
#error "ARG"
#endif

#include <cstddef>

namespace hg {

template <typename T> struct tVec2;
struct Vec4;

/// 3-Component vector
struct Vec3 {
	static const Vec3 Zero;
	static const Vec3 One;
	static const Vec3 Left, Right, Up, Down, Front, Back;
	static const Vec3 Min, Max;

	Vec3() = default;
	Vec3(float x, float y, float z);

	explicit Vec3(const tVec2<int> &v);
	explicit Vec3(const tVec2<float> &v);
	explicit Vec3(const float &v);
	explicit Vec3(const Vec4 &v);

	inline Vec3 &operator+=(const Vec3 &b) {
		x += b.x;
		y += b.y;
		z += b.z;
		return *this;
	}
	inline Vec3 &operator+=(const float k) {
		x += k;
		y += k;
		z += k;
		return *this;
	}
	inline Vec3 &operator-=(const Vec3 &b) {
		x -= b.x;
		y -= b.y;
		z -= b.z;
		return *this;
	}
	inline Vec3 &operator-=(const float k) {
		x -= k;
		y -= k;
		z -= k;
		return *this;
	}
	inline Vec3 &operator*=(const Vec3 &b) {
		x *= b.x;
		y *= b.y;
		z *= b.z;
		return *this;
	}
	inline Vec3 &operator*=(const float k) {
		x *= k;
		y *= k;
		z *= k;
		return *this;
	}
	inline Vec3 &operator/=(const Vec3 &b) {
		x /= b.x;
		y /= b.y;
		z /= b.z;
		return *this;
	}
	inline Vec3 &operator/=(const float k) {
		const float k_ = NotEqualZero(k) ? 1.F / k : 0.F;
		x *= k_;
		y *= k_;
		z *= k_;
		return *this;
	}

	inline Vec3 operator-() const {
		return Vec3(-x, -y, -z);
	}

	inline float operator[](size_t n) const {
		float res;

		if (n == 0) {
			res = x;
		} else if (n == 1) {
			res = y;
		} else if (n == 2) {
			res = z;
		} else {
			res = std::numeric_limits<float>::max();
		}

		return res;
	}

	inline float &operator[](size_t n) {
		float *res;

		if (n == 0) {
			res = &x;
		} else if (n == 1) {
			res = &y;
		} else if (n == 2) {
			res = &z;
		} else {
			res = nullptr;
		}

		return *res;
	}

	float x, y, z;
};

inline bool operator==(const Vec3 &a, const Vec3 &b) {
	return Equal(a.x, b.x) && Equal(a.y, b.y) && Equal(a.z, b.z);
}

inline bool operator!=(const Vec3 &a, const Vec3 &b) {
	return NotEqual(a.x, b.x) || NotEqual(a.y, b.y) || NotEqual(a.z, b.z);
}

inline Vec3 operator+(const Vec3 &a, const Vec3 &b) {
	return Vec3(a.x + b.x, a.y + b.y, a.z + b.z);
}

inline Vec3 operator+(const Vec3 &a, const float v) {
	return Vec3(a.x + v, a.y + v, a.z + v);
}

inline Vec3 operator-(const Vec3 &a, const Vec3 &b) {
	return Vec3(a.x - b.x, a.y - b.y, a.z - b.z);
}

inline Vec3 operator-(const Vec3 &a, const float v) {
	return Vec3(a.x - v, a.y - v, a.z - v);
}

inline Vec3 operator*(const Vec3 &a, const Vec3 &b) {
	return Vec3(a.x * b.x, a.y * b.y, a.z * b.z);
}

inline Vec3 operator*(const Vec3 &a, const float v) {
	return Vec3(a.x * v, a.y * v, a.z * v);
}

inline Vec3 operator*(const float v, const Vec3 &a) {
	return a * v;
}

inline Vec3 operator/(const Vec3 &a, const Vec3 &b) {
	return Vec3(a.x / b.x, a.y / b.y, a.z / b.z);
}

inline Vec3 operator/(const Vec3 &a, const float v) {
	return Vec3(a.x / v, a.y / v, a.z / v);
}

/// Return a random vector.
Vec3 RandomVec3(float min = -1.f, float max = 1.f);
Vec3 RandomVec3(const Vec3 &min, const Vec3 &max);

bool AlmostEqual(const Vec3 &a, const Vec3 &b, float epsilon);

/**
	@short Vector base to Euler.
	@note base convention u = {0,0,1}, v = {1,0,0}, second axis is optional.
*/
Vec3 BaseToEuler(const Vec3 &u);
Vec3 BaseToEuler(const Vec3 &u, const Vec3 &v);

/// Return hash of a vector.S
int Hash(const Vec3 &v);

/// Vector squared distance.
float Dist2(const Vec3 &a, const Vec3 &b);
/// Vector distance.
float Dist(const Vec3 &a, const Vec3 &b);

/// Squared vector length.
float Len2(const Vec3 &v);
/// Vector length.
float Len(const Vec3 &v);

/// Minimum of two vectors.
Vec3 Min(const Vec3 &a, const Vec3 &b);
/// Maximum of two vectors.
Vec3 Max(const Vec3 &a, const Vec3 &b);

/// Returns the dot product of two vectors.
inline float Dot(const Vec3 &a, const Vec3 &b) {
	return a.x * b.x + a.y * b.y + a.z * b.z;
}

/// Returns the cross product of two vectors.
inline Vec3 Cross(const Vec3 &a, const Vec3 &b) {
	return Vec3(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}

/// Returns the provided vector pointing in the opposite direction.
inline Vec3 Reverse(const Vec3 &v) {
	return Vec3(-v.x, -v.y, -v.z);
}

/// Returns the inverse of a vector.
inline Vec3 Inverse(const Vec3 &v) {
	return Vec3(1.F / v.x, 1.F / v.y, 1.F / v.z);
}

/// Normalize a vector.
Vec3 Normalize(const Vec3 &v);

/// Clamp vector.
Vec3 Clamp(const Vec3 &v, float min, float max);
/// Clamp vector component-wise.
Vec3 Clamp(const Vec3 &v, const Vec3 &min, const Vec3 &max);
/// Clamp vector length.
Vec3 ClampLen(const Vec3 &v, float min, float max);

/// Absolute vector.
Vec3 Abs(const Vec3 &v);
/// Sign vector.
Vec3 Sign(const Vec3 &v);

/// Return a unit vector reflected by a normal vector.
Vec3 Reflect(const Vec3 &v, const Vec3 &n);
/// Return a unit vector refracted around a normal vector.S
Vec3 Refract(const Vec3 &v, const Vec3 &n, float k_in = 1.f, float k_out = 1.f);

/// Returns a vector whose elements are equal to the nearest integer less than or equal to the vector elements.
Vec3 Floor(const Vec3 &v);
/// Returns a vector whose elements are equal to the nearest integer greater than or equal to the vector elements.
Vec3 Ceil(const Vec3 &v);

/**
	@short Return a vector which is facing a given direction.
	Returns a copy of this vector if it is already facing the given
	direction or the opposite of this vector otherwise.
*/
Vec3 FaceForward(const Vec3 &v, const Vec3 &d);

Vec3 MakeVec3(const Vec4 &v);

Vec3 Quantize(const Vec3 &v, float qx, float qy, float qz);
Vec3 Quantize(const Vec3 &v, float q);

/// Convert a triplet of angle in degrees to the Harfang unit system.
Vec3 Deg3(float x, float y, float z);
/// Convert a triplet of angle in radians to the Harfang unit system.
Vec3 Rad3(float x, float y, float z);

/// Return a vector from integer value in the [0;255] range.
inline Vec3 Vec3I(int x, int y, int z) {
	return Vec3(static_cast<float>(x) / 255.F, static_cast<float>(y) / 255.F, static_cast<float>(z) / 255.F);
}

} // namespace hg
